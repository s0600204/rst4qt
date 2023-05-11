#!/usr/bin/perl
use strict;
use warnings;

use Dpkg::Control::Info;
use Dpkg::Deps;

my $control_info = Dpkg::Control::Info->new();
my $control_fields = $control_info->get_source();
my $build_depends = deps_parse($control_fields->{'Build-Depends'});

print deps_concat($build_depends);
