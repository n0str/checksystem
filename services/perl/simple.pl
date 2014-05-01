#!/usr/bin/perl

use warnings;
use strict;
use AnyEvent;
use AnyEvent::Util;
use IO::Socket::INET;
use MIME::Base64;
use Term::ANSIColor;

$AnyEvent::Util::MAX_FORKS = 31;

my %global_user_db = ();

my $server = IO::Socket::INET->new(
        'Proto'     => 'tcp',
        'LocalAddr' => 'localhost',
        'LocalPort' => 0x4014,
        'Listen'    => 3,
        'ReuseAddr' => 1
    ) or die $!;

my $cv = AnyEvent->condvar;

my $handle_client = AnyEvent->io(
        fh      => \*{$server},
        poll    => 'r',
        cb      => sub {
            $cv->begin();
            fork_call \&handle_connections, $server->accept, \&handle_token;
        }
    );


sub welcome_msg($) {
    my $client = shift;

    print $client "Welcome to the 'Notes collection' service!\n",
                  "Possible actions now are : auth, reg\n",
                  "\$ ";
}

sub parse_user_credentials($) {
    my $response = shift;

    my ($plain_token_data, $plain_user_name) = unpack "H32H*", decode_base64($response);
    my ($user_token, $user_name) = ("", "");

    map $user_token.= chr hex, (map $_, $plain_token_data =~ /(..)/g);
    map $user_name .= chr (hex ^ 0xBB), reverse (map $_, $plain_user_name =~ /(..)/g);

    $user_name =~ s/[^|\w ]//g;

    ($user_name, $user_token);
}

sub get_user_info($) {
    my $client = shift;

    print $client "--> Now send me your token\n# ";
    my $user_token = <$client>;
    
    if (not defined $user_token) {
        return (undef, undef);
    }

    if (scalar(split //, $user_token) < 0x14) {
        return (undef, undef);
    }

    chomp $user_token;
    parse_user_credentials($user_token);
}

sub check_user_id($) {
    my $client = shift;

    my ($user_name, $token_id) = get_user_info($client);

    if (not defined $user_name or not defined $token_id) {
        return undef;
    }

    if (not exists $global_user_db{$user_name}) {
        return undef;
    }

    if ($global_user_db{$user_name} ne $token_id) {
        return undef;
    }

    return $user_name;
}

sub get_user_name($) {
    my $client = shift;

    print $client "--> Enter your name (4 or more chars)\n# ";
    my $user_name = <$client>;

    return undef if not defined $user_name;

    chomp $user_name;
    $user_name =~ s/[^|\w ]//g;

    return undef if length $user_name < 5;

    ($user_name) = $user_name =~ /^(.{5,15}).*/;

    return $user_name;
}

sub generate_user_id($) {
    my $user_name   = shift;
    my @time_values = unpack "(H2)*", time;

    srand int(hex $time_values[6] * hex $time_values[7]);

    my $user_id = "";

    map $user_id.=chr(int(rand(255)) ^ ord((split //, $user_name)[$_ % length $user_name])), (0 .. 15);

    $user_id;
}

sub create_new_user($) {
    my $client = shift;

    my $user_name = get_user_name($client);

    if (not defined $user_name) {
        print $client "--> Wrong user name\n";
        return (undef, undef, undef);
    }

    if (exists $global_user_db{$user_name}) {
        print $client "--> User already exist\n";
        return (undef, undef, undef);
    }

    my $user_id    = generate_user_id($user_name);
    my $user_token = $user_id.join "", map chr(hex ^ 0xBB), reverse (unpack("H*", $user_name) =~ /(..)/g);   

    return ($user_id, $user_name, $user_token);
}

sub handle_unauth_cmd($$$) {
    my ($client, $cmd, $state) = @_;

    if ($cmd =~ /^auth$/) {
        my $user_name = check_user_id($client);

        if (not defined $user_name) {
            print $client "--> Wrong token\n\$ ";
            return undef;
        }

        print $client "Hello $user_name\n$user_name \$ ";

        $$state{auth} = 1;
        $$state{name} = $user_name;

        return $user_name;
    }

    if ($cmd =~ /^reg$/) {
        my ($user_id, $user_name, $user_token) = create_new_user($client);

        if (not defined $user_name or not defined $user_id or not defined $user_token) {
            print $client "--> New account was not created\n\$ ";
            return undef;
        }

        $$state{auth}     = 1;
        $$state{name}     = $user_name;
        $$state{token_id} = $user_id;

        print $client "--> Your token is ".encode_base64($user_token).$user_name." \$ ";

        return $user_name;
    }

    print $client "Unknown command\n\$ ";
}

sub handle_connections($) {
    my $client = shift;

    print "new connection\n";

    welcome_msg($client);

    my %user_credentials = (auth => 0, name => undef, token_id => undef);

    while (my $client_response = <$client>) {

        if ($user_credentials{'auth'} == 0) {
            handle_unauth_cmd($client, $client_response, \%user_credentials);
            next;
        }

        print $client "Unknown command\n$user_credentials{name} \$ ";
    }

    $cv->end();

    ($user_credentials{name}, $user_credentials{token_id});
}

sub handle_token($$) {
    my ($user_name, $token_id) = @_;
    print "connection was closed\n";

    if (defined $user_name and defined $token_id) {
        $global_user_db{$user_name} = $token_id if not exists $global_user_db{$user_name};
    }
}

$cv->recv();