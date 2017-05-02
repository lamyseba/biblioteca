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
   Tellico XSLT file - Calandreta Fiches Report par Sébastien Lamy
   <lamyseba@free.fr>
   Combiné avec un fichier base de donnée de livre tellico au format 
   XML, Ce fichier XSLT permet de générer le document HTML qui affiche 
   les fiches des livres. C'est le fichier HTML (affichable dans un 
   navigateur) qui est ensuite utilisé pour générer un PDF (destiné
   à l'impression)

   Inspired by Column View Report and Title_Listing (Horizontal) Reports 
   from Robby Stephenson <robby@periapsis.org>

   This XSLT stylesheet is designed to be used with the 'Tellico'
   application, which can be found at http://tellico-project.org

   ===================================================================
-->

<!-- import common templates -->
<!-- location depends on being installed correctly -->
<xsl:import href="ressources/tellico-common.xsl"/>            
<xsl:include href="calandreta_utils.xsl"/>

<!-- set the maximum image size -->
<xsl:param name="image-height" select="'100'"/>
<xsl:param name="image-width" select="'100'"/>

<!-- Le nombre de fiches par ligne -->
<xsl:variable name="num-columns" select="4"/>

<xsl:template match="/">
 <xsl:apply-templates select="tc:tellico"/>
</xsl:template>


<xsl:template match="tc:tellico">
 <html>
  <head>
   <!-- Désigne le fichier de mise en forme des fiches (couleurs, polices, marges, etc...) -->
   <link rel="stylesheet" type="text/css" href="fiches.css"/>
   <title>
    <xsl:value-of select="tc:collection/@title"/> - Fiches à imprimer
   </title>
  </head>
  <body><xsl:apply-templates select="exsl:node-set($sorted-entries)/tc:entry"/></body>
 </html>
</xsl:template>


<!-- La fiche qui correspond à un livre -->
<xsl:template match="tc:entry">
  <xsl:variable name="entry" select="."/>
  <xsl:variable name="col_index" select="((position()-1) mod $num-columns) + 1"/>
  <xsl:variable name="row_page_position" select="floor((position()-1) div $num-columns) mod 2"/>
  <div class="fiche rpp{$row_page_position} col{$col_index}">

  <!-- title field (with property index_card=title)-->
  <xsl:variable name="title_field" select="$fields_props[.='title'][1]/.."/>
  <div class="field_name"><xsl:value-of select="$title_field/@title"/>&#160;: </div>
  <h2><xsl:call-template name="fieldValue">
    <xsl:with-param name="entry" select="$entry"/>
    <xsl:with-param name="field" select="$title_field"/>
  </xsl:call-template></h2>
  
  <!-- primary fields (with property index_card=primary)-->
  <div class="primary">
  <xsl:for-each select="$fields_props[.='primary']/..">
    <div class="field">
    <xsl:variable name="field" select="."/>
    <span class="field_name"><xsl:value-of select="$field/@title"/>&#160;: </span>
    <span class="field_content"><xsl:call-template name="fieldValue">
      <xsl:with-param name="entry" select="$entry"/>
      <xsl:with-param name="field" select="$field"/>
    </xsl:call-template></span>
    </div>
  </xsl:for-each>
  </div>

  <!-- separator -->
  <div class="separator">-----</div>
 
  <!-- secondary fields (with property index_card=secondary) -->
  <div class="secondary">
    <xsl:for-each select="$fields_props[.='secondary']">
      <div>
      <xsl:variable name="field" select=".."/>
      <span class="field_name"><xsl:value-of select="$field/@title"/>&#160;: </span>
      <span class="field_content"><xsl:call-template name="fieldValue">
        <xsl:with-param name="entry" select="$entry"/>
        <xsl:with-param name="field" select="$field"/>
      </xsl:call-template></span>
      </div>
    </xsl:for-each>
  </div>
  </div>
</xsl:template>



<!-- Affiche la valeur d'un champs dans la fiche -->
<xsl:template name="fieldValue">
 <xsl:param name = "entry"/>
 <xsl:param name="field"/>

 <!-- Count the number of values for that field in that entry: -->
    <!-- stick all the descendants into a variable -->
 <xsl:variable name="current" select="$entry/descendant::*"/>
    <!-- find all descendants whose name matches the column name -->
 <xsl:variable name="numvalues" select="count($current[local-name() = $field/@name])"/>

 <xsl:choose>
    <!-- when there is more than one value... -->
    <xsl:when test="$numvalues &gt; 1">
     <xsl:call-template name="simple-field-value">
      <xsl:with-param name="entry" select="$entry"/>
      <xsl:with-param name="field" select="$field/@name"/>
     </xsl:call-template>
    </xsl:when>
    
    <!-- when there is only one value -->
    <xsl:when test="$numvalues = 1">
     <xsl:for-each select="$current[local-name() = $field/@name]">
      <xsl:choose>       
       <!-- check for images -->
       <xsl:when test="$field/@type=10">
        <xsl:attribute name="style">
         <xsl:text>text-align: center; padding-left: 5px</xsl:text>
        </xsl:attribute>
        <img>
         <xsl:attribute name="src">
          <xsl:call-template name="image-link">
           <xsl:with-param name="image" select="key('imagesById', .)"/>
           <xsl:with-param name="dir" select="$imgdir"/>
          </xsl:call-template>
         </xsl:attribute>
         <xsl:call-template name="image-size">
          <xsl:with-param name="limit-width" select="$image-width"/>
          <xsl:with-param name="limit-height" select="$image-height"/>
          <xsl:with-param name="image" select="key('imagesById', .)"/>
         </xsl:call-template>
        </img>
       </xsl:when>

       <!-- handle URL here, so no link created -->
       <xsl:when test="$field/@type=7">
        <xsl:value-of select="."/>
       </xsl:when>

       <!-- finally, it's just a regular value -->
       <xsl:otherwise>
        <xsl:call-template name="simple-field-value">
         <xsl:with-param name="entry" select="$entry"/>
         <xsl:with-param name="field" select="$field/@name"/>
        </xsl:call-template>
       </xsl:otherwise>

      </xsl:choose>
     </xsl:for-each>
    </xsl:when>    
    
    <!-- when there is no value -->
    <xsl:otherwise>
     <xsl:text> </xsl:text>
    </xsl:otherwise>
   </xsl:choose>  
</xsl:template>

</xsl:stylesheet>
<!-- Local Variables: -->
<!-- sgml-indent-step: 1 -->
<!-- sgml-indent-data: 1 -->
<!-- End: -->
