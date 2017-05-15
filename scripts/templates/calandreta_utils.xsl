<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tc="http://periapsis.org/tellico/"
                xmlns:str="http://exslt.org/strings"
                xmlns:dyn="http://exslt.org/dynamic"
                xmlns:exsl="http://exslt.org/common"
                extension-element-prefixes="str dyn exsl"
                exclude-result-prefixes="tc"
                version="1.0">

<!--
   ===================================================================
   Tellico XSLT file - Utilities templates for Calandreta Reports
   
   Tri de l'ordre d'impression, gestion des livres pour lesquels il 
   faut imprimer plusieurs fiches ou cotes, filtrage des fiches ou 
   cotes à imprimer

   Copyright (C) 2017 Sébastien Lamy <lamyseba@free.fr>

   This XSLT stylesheet is designed to be used with the 'Tellico'
   application, which can be found at http://tellico-project.org
   ===================================================================
-->

<xsl:output method="html"
            indent="no"
            doctype-public="-//W3C//DTD HTML 4.01//EN"
            doctype-system="http://www.w3.org/TR/html4/strict.dtd"
            encoding="utf-8"/>

<!-- On ne travaille que parmi les entrées filtrées par la condition
     (exemple de condition: 
        //dont on doit imprimer au moins une fiche
      [@id &gt; 80]  //dont le numéro d'index est supérieur à 80
      -->
<xsl:param name="entry_predicate"/>


<!-- Up to three fields may be used for sorting. -->
<xsl:param name="sort-name1" select="'title'"/>
<xsl:param name="sort-name2" select="''"/>
<xsl:param name="sort-name3" select="''"/>
<!-- This is the title just beside the collection name. It will
     automatically list which fields are used for sorting. -->
<xsl:param name="sort-title" select="''"/>
<!-- Sort using user's preferred language -->
<xsl:param name="lang"/>

<xsl:param name="datadir"/> <!-- dir where Tellico data files are located -->
<xsl:param name="imgdir"/> <!-- dir where field images are located -->

<xsl:key name="fieldsByName" match="tc:field" use="@name"/>
<xsl:key name="entriesById" match="tc:entry" use="@id"/>
<xsl:key name="imagesById" match="tc:image" use="@id"/>

<!-- In case the field has multiple values, only sort by first one -->
<xsl:variable name="sort1">
 <xsl:if test="string-length($sort-name1) &gt; 0">
  <xsl:value-of select="concat('.//tc:', $sort-name1, '[1]')"/>
 </xsl:if>
</xsl:variable>

<xsl:variable name="sort1-type">
 <xsl:choose>
  <xsl:when test=".//tc:field[@name=$sort-name1]/@type = 6">number</xsl:when>
  <xsl:otherwise>text</xsl:otherwise>
 </xsl:choose>
</xsl:variable>

<xsl:variable name="sort2">
 <xsl:if test="string-length($sort-name2) &gt; 0">
  <xsl:value-of select="concat('.//tc:', $sort-name2, '[1]')"/>
 </xsl:if>
</xsl:variable>

<xsl:variable name="sort2-type">
 <xsl:choose>
  <xsl:when test=".//tc:field[@name=$sort-name2]/@type = 6">number</xsl:when>
  <xsl:otherwise>text</xsl:otherwise>
 </xsl:choose>
</xsl:variable>

<xsl:variable name="sort3">
 <xsl:if test="string-length($sort-name3) &gt; 0">
  <xsl:value-of select="concat('.//tc:', $sort-name3, '[1]')"/>
 </xsl:if>
</xsl:variable>

<xsl:variable name="sort3-type">
 <xsl:choose>
  <xsl:when test=".//tc:field[@name=$sort-name3]/@type = 6">number</xsl:when>
  <xsl:otherwise>text</xsl:otherwise>
 </xsl:choose>
</xsl:variable>

<!-- Les champs qu'on doit imprimer sur la fiche ont une propriété 'index_card' -->
<xsl:variable name="fields_props" select="//tc:field/tc:prop[@name='index_card']"/>

<!-- Le chemin des enregistrement de livre dans le fichier xml de tellico -->
<xsl:variable name="entry_path" select="'/tc:tellico/tc:collection/tc:entry'"/>

<!-- a sorted list, filtered by $entry_predicate and with entries duplicated if we need it-->
<xsl:variable name="sorted-entries">
 <xsl:for-each select="dyn:evaluate(concat($entry_path,$entry_predicate))"> 
  <xsl:sort lang="$lang" select="dyn:evaluate($sort1)" data-type="{$sort1-type}"/>
  <xsl:sort lang="$lang" select="dyn:evaluate($sort2)" data-type="{$sort2-type}"/>
  <xsl:sort lang="$lang" select="dyn:evaluate($sort3)" data-type="{$sort3-type}"/>   
   
  <xsl:call-template name="handleCopies">
   <xsl:with-param name="entry" select="." />
   <xsl:with-param name="copies_count" select="./tc:nb-ex" />
  </xsl:call-template>
 </xsl:for-each>
</xsl:variable>



<!-- copy recursively an entry, this is for handling entries 
     with multiple copies in the collection -->
<xsl:template name="handleCopies">
    <xsl:param name="entry" />
    <xsl:param name="copies_count" />
    <xsl:copy-of select="$entry"/>
    <!-- Tant que le nombre de copie n'est pas sorti, on continue à copier -->
    <xsl:if test="$copies_count &gt; 1">
      <xsl:call-template name="handleCopies">
        <xsl:with-param name="entry" select="$entry" />
        <xsl:with-param name="copies_count" select="$copies_count - 1"/>
      </xsl:call-template>
    </xsl:if>
</xsl:template>

</xsl:stylesheet>