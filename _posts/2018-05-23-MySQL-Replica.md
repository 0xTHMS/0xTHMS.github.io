---
layout: post
title: pt-table-checksum - Surveiller l'intégrité de ses bases mysql
date: 2018-05-23 16:33:33
author: thms
tags: mysql percona master slave pt-table-checksum checksum replication integrity integrite
---

# Introduction
J'ai récemment dû mettre en place une réplication MySQL 5.1 master/slave pour le compte d'un client afin de mener à bien une migration.
Lors de la préparation de la migration, je voulais trouver un moyen de m'assurer que ma replication était correct et que le serveur de destination était intègre.

A ma connaissance, mysql n'intègre pas d'outil permettant de vérifier ceci, mais c'est le cas de Percona, qui contient un outil nommé `pt-table-checksum` dans son paquet `perconna-toolkit` et qui reste complètement compatible avec MySQL, même en version 5.1

Par ailleurs, les outils percona sont très pratiques, il est possible d'effectuer des check locaux, mais aussi d'aller interroger d'autres serveurs qui n'ont pas forcément la suite percona d'installée.

Cet article consitue donc un mémo sur le sujet.

# Installation & configuration
{% highlight bash %}
apt-get install percona-toolkit
{% endhighlight %}

On créé une table qui contiendra la liste des slaves à vérifier.
{% highlight sql %}
CREATE TABLE `dsns` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT NULL,
  `dsn` varchar(255) NOT NULL,
   PRIMARY KEY (`id`));
{% endhighlight %}

