# /etc/puppetlabs/puppet/modules/apache/manifests/vhost.pp
define apache::vhost (
  Integer $port,
  String[1] $docroot,
  String[1] $servername = $title,
  String $vhost_name = '*',
) {
  include apache # contains package['httpd'] and service['httpd']
  include apache::params # contains common config settings

  $vhost_dir = $apache::params::vhost_dir

  # the template used below can access all of the parameters and variable from above.
  file { "${vhost_dir}/${servername}.conf":
    ensure  => file,
    owner   => 'www',
    group   => 'www',
    mode    => '0644',
    content => template('apache/vhost-default.conf.erb'),
    require  => Package['httpd'],
    notify    => Service['httpd'],
  }
}