# == Class: cdh::sqoop
#
# Installs Sqoop 1
#
# === Parameters
#
# [*sqoop_metastore_client_autoconnect_url*]
#   The connect string to use when connecting to a job-management metastore. Default: undef
#
# [*sqoop_metastore_client_record_password*]
#   If true, allow saved passwords in the metastore. Default: true
#
class cdh::sqoop(
    $hadoop_opts                            = $::cdh::sqoop::defaults::hadoop_opts,
    $sqoop_metastore_client_autoconnect_url = $::cdh::sqoop::defaults::sqoop_metastore_client_autoconnect_url,
    $sqoop_metastore_client_record_password = $::cdh::sqoop::defaults::sqoop_metastore_client_record_password
) {
    # Sqoop requires Hadoop configs installed.
    Class['cdh::hadoop'] -> Class['cdh::sqoop']

    package { 'sqoop':
        ensure => 'installed',
    }

    if (!defined(Package['libmysql-java'])) {
        package { 'libmysql-java':
            ensure => 'installed',
        }
    }
    # symlink the mysql-connector-java.jar that is installed by
    # libmysql-java into /usr/lib/sqoop/lib
    # TODO: Can I create this symlink as mysql.jar?
    file { '/usr/lib/sqoop/lib/mysql-connector-java.jar':
        ensure  => 'link',
        target  => '/usr/share/java/mysql-connector-java.jar',
        require => [Package['sqoop'], Package['libmysql-java']],
    }

    $config_directory = "/etc/sqoop/conf.${cdh::hadoop::cluster_name}"
    # Create the $cluster_name based $config_directory.
    file { $config_directory:
        ensure  => 'directory',
        require => Package['sqoop']
    }
    cdh::alternative { 'sqoop-conf':
        link    => '/etc/sqoop/conf',
        path    => $config_directory,
        require => File[$config_directory]
    }

    file { "${config_directory}/sqoop-env.sh":
        content => template('cdh/sqoop/sqoop-env.sh.erb'),
        require => [Package['sqoop'], File[$config_directory]]
    }
    file { "${config_directory}/sqoop-site.xml":
        content => template('cdh/sqoop/sqoop-site.xml.erb'),
        require => [Package['sqoop'], File[$config_directory]]
    }
}
