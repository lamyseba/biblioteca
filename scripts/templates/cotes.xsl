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
   Tellico XSLT file - Cotes Report par Sébastien Lamy
   <lamyseba@free.fr>
   Combiné avec un fichier base de donnée de livre tellico au format 
   XML, Ce fichier XSLT permet de générer le document HTML qui affiche 
   les cotes des livres. C'est le fichier HTML (affichable dans un 
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
<xsl:import href="tellico-common.xsl"/>            
<xsl:include href="calandreta_utils.xsl"/>


<xsl:template match="/">
 <xsl:apply-templates select="tc:tellico"/>
</xsl:template>

<xsl:template match="tc:tellico">
 <html>
  <head>
   <!-- Désigne le fichier de mise en forme des fiches (couleurs, polices, marges, etc...) -->   
   <link rel="stylesheet" type="text/css" href="cotes.css"/>
   <title>
    <xsl:value-of select="tc:collection/@title"/> - Cotes à imprimer
   </title>
  </head>  
  <body><xsl:apply-templates select="exsl:node-set($sorted-entries)/tc:entry"/></body>
 </html>
</xsl:template>

<!-- La cote qui correspond à un livre -->
<xsl:template match="tc:entry">
  <xsl:variable name="cote" select="./tc:cote"/>
  <xsl:choose>
    <xsl:when test="not($cote)"></xsl:when>
    <xsl:when test="./tc:genre='Album' and string-length($cote)=1">
        <div class="cote album"><span><xsl:value-of select="$cote"/></span></div>
    </xsl:when>
    <xsl:otherwise>
        <xsl:variable name="cote_lines" select="str:tokenize($cote)"/>
        <div class="cote generale"><span>
            <xsl:value-of select="$cote_lines[1]"/><br/>
            <xsl:value-of select="$cote_lines[2]"/></span>
        </div>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>




</xsl:stylesheet>
<!-- Local Variables: -->
<!-- sgml-indent-step: 1 -->
<!-- sgml-indent-data: 1 -->
<!-- End: -->
