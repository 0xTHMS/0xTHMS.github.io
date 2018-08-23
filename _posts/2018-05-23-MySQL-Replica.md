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
CREATE DATABASE PERCONA;
CREATE TABLE `dsns` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT NULL,
  `dsn` varchar(255) NOT NULL,
   PRIMARY KEY (`id`));
{% endhighlight %}


Ensuite, insérer les hôtes à surveiller dans cette table. (INSERT INTO ..)
{% highlight sql %}
   INSERT INTO dsns SET dsn = 'h=<IP_SLAVE>,u=<UTILISATEUR>,p=toto123'
{% endhighlight %}


# Utilisation

Voici ce à quoi la table dsns peut ressembler une fois peuplée:
{% highlight %}
  mysql> select * from dsns;
+----+-----------+----------------------------------------------------+
| id | parent_id | dsn                                                |
+----+-----------+----------------------------------------------------+
|  1 |      NULL | h=xx.xxx.xxx.229,u=checksum,p=motdepassequitue!!!! |
|  2 |      NULL | h=xx.xxx.xxx.230,u=checksum,p=motdepassequitue!!!! |
+----+-----------+----------------------------------------------------+
{% endhighlight %}

Ici, il s'agit d'un setup master/slave mysql 5.1

Je peux ensuite lancer le check d'intégrité avec la commande suivante:
{% highlight bash %}
  pt-table-checksum --replicate=percona.checksums --ignore-databases mysql h=localhost,u=checksum,p=password --recursion-method dsn=D=percona,t=dsns
{% endhighlight %}

avec "h=localhost,u=checksum,p=password" j'indique les informations de connexion au serveur ou on trouve la table `dsns`

L'outil va ensuite se connecter aux master et au slave, et commencer le check d'intégrité et la comparaison de toutes les bases, sauf celle nommée mysql (puisque je choisi de l'ignorer)
