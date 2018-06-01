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
{% highlight %}

On créé une table qui contiendra la liste des slaves à vérifier.
{% highlight sql %}
CREATE TABLE `dsns` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT NULL,
  `dsn` varchar(255) NOT NULL,
   PRIMARY KEY (`id`));
{% highlight %}


# Astuces
Lors de la connnexion à un hote derrière le bastion SSH,  on doit d'abord se connecter sur le bastion, puis se connecter sur l'hote final.

{% highlight bash %}

thms@home> ssh thms@bastion
thms@bastion> ssh thms@10.0.0.1

{% endhighlight %}

Afin de gagner du temps, il est beaucoup plus pratique d'effectuer #2 directement.

Pour se faire, on va éditer le fichier `.ssh/config`:

{% highlight bash %}
Host bastion
 IdentityFile ~/.ssh/id_rsa
 User thms

Host 10.0.*.*
 IdentityFile ~/.ssh/id_rsa
 ProxyCommnd ssh thms@bastion -W %h:%p
 User root
{% endhighlight %}

Le premier block permet de se connecter au bastion grace à la clé `id_rsa`, en tant qu'utilisateur `thms`

Le second block permet de dire au client SSH "pour chaque IP qui *match* 10.0.*.*", on se connecte via `bastion`, avec la clé renseignée dans IdentityFile

Ainsi, lorsque j'écris `ssh bastion`, mon client ssh se connecte en tant que thms à bastion avec ma clé.

De même, lorsque j'écris `ssh 10.0.0.1`, mon client SSH se connecte à bastion et initie la connexion depuis bastion, en tant qu'utilisateur root, vers 10.0.0.1

