---
layout: post
title: Restricted shells & shell escapes 
date: 2018-08-23 16:33:33
author: thms
tags: bash rbash rsh sh shell escapes vim tar zip 
---

# Restricted shells

( Toujours pas fini cet article ... )

Je suis récemment tombé sur un challenge qui nécessitait de sortir d'un shell restreint.

Celui-ci m'a permis de (re)découvrir de nombreuses façon de s'échapper d'un tel shell. 
Ce post a pour but d'être un mémo sur le sujet et de référencer toutes les manières connues permettant ce bypass.


# vim
{% highlight bash %}
:set shell=/bin/bash
:shell
{% endhighlight %}

# tar
{% highlight bash %}
tar --checkpoint-action=exec=/bin/bash --checkpoint=1 
{% endhighlight %}

# man
{% highlight bash %}
test
{% endhighlight %}
