---
layout: post
title: Recovering from a MySQL crash 
date: 2018-10-10 16:33:33
author: thms
tags: mysql mariadb debian sql database sysadmin recovering mysqlcheck 
---

# Vérifier l'espace disque de la partition mysql
{% highlight bash %}
df -h
{% endhighlight %}

Le mieux étant d'avoir une partition séparée pour mysql


# Regarder les logs
Les logs vont souvent être une préciseuse source d'informations
{% highlight bash %}
grep mysql /var/log/syslog
{% endhighlight %}

Je ne peux vous montrer d'extrait, car les messages d'erreurs peuvent être tellement différents.
Une fois le message en main, Google est votre ami

# Utilser mysqlcheck
Mysqlcheck est un outil intégré a mysql qui permet de réparer une ou plusieurs bases.
{% highlight bash %}
mysqlcheck --defaults-file=/etc/mysql/debian.cnf
{% endhighlight %}

# Utilise mysqlrepair
Mysqlrepair est similaire a mysqlcheck

# Si mySQL ne démarre pas
Alors, dans ce cas, l'option
{% highlight bash %}
innodb_force_recovery
{% endhighlight %}

est à essayer

