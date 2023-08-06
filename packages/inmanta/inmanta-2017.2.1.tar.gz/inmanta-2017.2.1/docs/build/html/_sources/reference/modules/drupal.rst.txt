Module drupal
=============

 * License: Apache 2.0
 * Version: 0.4.0
 * Author: Inmanta <code@inmanta.com>
 * Upstream project: https://github.com/inmanta/drupal.git

Entities
--------

.. inmanta:entity:: drupal::Application

   Parents: :inmanta:entity:`php::Application`

   A single drupal application
   

   .. inmanta:attribute:: string drupal::Application.site_name


   .. inmanta:attribute:: string drupal::Application.admin_email


   .. inmanta:attribute:: string drupal::Application.admin_user


   .. inmanta:attribute:: string drupal::Application.admin_password


   .. inmanta:relation:: mysql::Database drupal::Application.database [1]

      other end: :inmanta:relation:`mysql::Database.drupal_app [0:\*]<mysql::Database.drupal_app>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`drupal::drupalSiteRPM`
      * :inmanta:implementation:`drupal::drupalSiteDEB`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`drupal::drupalSiteRPM`, :inmanta:implementation:`php::phpApacheRPM`, :inmanta:implementation:`apache::appImplRPM`
        constraint ``(std::familyof(container.host.os,'rhel') or std::familyof(container.host.os,'fedora'))``
      * :inmanta:implementation:`drupal::drupalSiteDEB`, :inmanta:implementation:`php::phpApacheDEB`, :inmanta:implementation:`apache::appImplDEB`
        constraint ``std::familyof(container.host.os,'ubuntu')``


Implementations
---------------

.. inmanta:implementation:: drupal::drupalSiteDEB

.. inmanta:implementation:: drupal::drupalSiteRPM
