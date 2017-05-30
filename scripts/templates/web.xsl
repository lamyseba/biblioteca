<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tc="http://periapsis.org/tellico/"
                xmlns:str="http://exslt.org/strings"
                xmlns:dyn="http://exslt.org/dynamic"
                extension-element-prefixes="str dyn"
                exclude-result-prefixes="tc"
                version="1.0">

<!--
   ===================================================================
   Tellico XSLT file - Column View Report

   Copyright (C) 2005-2009 Robby Stephenson <robby@periapsis.org>

   This XSLT stylesheet is designed to be used with the 'Tellico'
   application, which can be found at http://tellico-project.org

   ===================================================================
-->

<!-- import common templates -->
<!-- location depends on being installed correctly -->
<xsl:import href="tellico-common.xsl"/>

<xsl:output method="html"
            indent="yes"
            doctype-public="-//W3C//DTD HTML 4.01//EN"
            doctype-system="http://www.w3.org/TR/html4/strict.dtd"
            encoding="utf-8"/>

<xsl:param name="filename"/>
<xsl:param name="cdate"/>

<!-- To choose which fields of each entry are printed, change the
     string to a space separated list of field names. To know what
     fields are available, check the Tellico data file for <field>
     elements. -->
<xsl:param name="column-names" select="'title'"/>
<xsl:variable name="columns" select="str:tokenize($column-names)"/>

<!-- set the maximum image size -->
<xsl:param name="image-height" select="'100'"/>
<xsl:param name="image-width" select="'100'"/>

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

<xsl:variable name="lowercase" select="'aáàâbcçdeéèêfghiíîjklmnoóòôpqrstuúùûvwxyzÁÂÇÉÈÊÍÎÓÒÔÚÛ'"/>
<xsl:variable name="uppercase" select="'AAAABCCDEEEEFGHIIIJKLMNOOOOPQRSTUUUUVWXYZAACEEEIIOOOUU'"/>

<xsl:template match="/">
 <xsl:apply-templates select="tc:tellico"/>
</xsl:template>

<xsl:template match="tc:tellico">
 <html>
  <head>
   <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/v/dt/jqc-1.12.4/dt-1.10.13/b-html5-1.2.4/b-print-1.2.4/fh-3.1.2/datatables.min.css"/>
   <script type="text/javascript" src="https://cdn.datatables.net/v/dt/jqc-1.12.4/dt-1.10.13/b-html5-1.2.4/b-print-1.2.4/fh-3.1.2/datatables.min.js"></script>

   <style type="text/css">
   body {font-family: sans-serif;<xsl:if test="count($columns) &gt; 3">font-size: 80%;</xsl:if>background-color: #fff;margin:0}
   #header-left {
        margin-top: 0;
        float: left;
        padding:8px;
   }
   #header-right {
        margin: 0 0 0 30px;
        float: right;
        display: block;
        padding: 12px 20px 12px 50px;
        color: #fff;
        background: url('blacktobook.svg') #444 no-repeat 8% 50%;
        background-size: 35px;
        font-weight: 700;
        border: none;
        text-decoration: none;
        font-size:15px;
   }
   #header-right:hover{background-color:#1883ed}
   h1.colltitle {        
        margin: 0 0 5px 0;
        padding: 6px;
        font-size: 2em;
        text-align: center;
        background-color: #212121;
   }
   #header-left, #header-right, h1.colltitle{color:#fff;}
   
   table {
        margin-left: auto;
        margin-right: auto;
   }
   /*th {
        color: #000;
        background-color: #ccc;
        border: 1px solid #999;
        font-size: 1.1em;
        font-weight: bold;
        padding-left: 4px;
        padding-right: 4px;
   }*/
   tr.r0 {
   }
   tr.r1 {
        background-color: #eee;
   }
   td.field {
        margin-left: 0px;
        margin-right: 0px;
        padding-left: 5px;
        padding-right: 5px;
        border: 1px solid #eee;
        text-align: left;
   }
   #myTable_length, #myTable_filter{
    float:none;
    display:inline-block;
   }
   #myTable_filter{margin-right:30px;text-align:left;}
   #myTable_filter,#myTable_info{margin-left:10px;}
   #myTable_paginate{padding-top:0}
   </style>
   
   
   <script type="text/javascript" class="init"><xsl:text disable-output-escaping="yes" ><![CDATA[
    jQuery.fn.DataTable.ext.type.search.string = function ( data ) {
        return ! data ?
        '' :
        typeof data === 'string' ?
            data
                .replace( /\n/g, ' ' )
                .replace( /[áàäâ]/g, 'a' )
                .replace( /[ÁÀÄÂ]/g, 'A' )
                .replace( /[éèëê]/g, 'e' )
                .replace( /[ÉÈËÊ]/g, 'E' )
                .replace( /[íìïî]/g, 'i' )
                .replace( /[ÍÌÏÎ]/g, 'I' )
                .replace( /[óòöô]/g, 'o' )
                .replace( /[ÓÒÖÔ]/g, 'O' )
                .replace( /[úùüû]/g, 'u' )
                .replace( /[ÚÙÜÛ]/g, 'U' )
                .replace( /ñ/g, 'n' )
                .replace( /Ñ/g, 'N' )
                .replace( /ç/g, 'c' )
                .replace( /Ç/g, 'C' ):
            data;
    };
    $(document).ready(function() {
      $('#myTable').DataTable( {
        "dom":'pflrtip',
        "columnDefs": [
            { "type": "string", "targets": [1,2,3,4,5,6,8] }
        ],
        "language": {
          processing:     "Traitement en cours...",
          search:         "Cercar&nbsp;:",
          lengthMenu:    "Afichar _MENU_ elements",
          info:           "Afichatge de l'element _START_ a _END_ sus _TOTAL_ elements",
          infoEmpty:      "Afichatge de 0 element 0 sus 0 element",
          infoFiltered:   "(filtrats de _MAX_ elements en tot)",
          infoPostFix:    "",
          loadingRecords: "Chargement en cours...",
          zeroRecords:    "Non i a pas arren que afichar",
          emptyTable:     "Aucune donnée disponible dans le tableau",
          paginate: {
            first:      "&nbsp;|<&nbsp;" /*"Prum&eagrave;r"*/,
            previous:   "&nbsp;<&nbsp;" /*"Precedent"*/,
            next:       "&nbsp;>&nbsp;" /*"Seguent"*/,
            last:       "&nbsp;>|&nbsp;" /*"Darr&eagrave;r"*/
          },
          aria: {
            sortAscending:  ": activer pour trier la colonne par ordre croissant",
            sortDescending: ": activer pour trier la colonne par ordre décroissant"
          }
        },
        "lengthMenu":    [[15, 25, 100, -1], [10, 25, 100, "Tous"]],
        "pageLength":    25,
        "pagingType":    'full',
        "order":[],
        "orderClasses": false,        
        "fixedHeader":true
      } );
      

      // Remove accented character from search input as well
      $('#myTable_filter input[type=search]').keyup( function () {
        var table = $('#myTable').DataTable();
        table
          .search(
            jQuery.fn.DataTable.ext.type.search.string( this.value )
          )
          .draw()
      } );
     } );]]></xsl:text></script>
   <title>
    <xsl:value-of select="tc:collection/@title"/>
   </title>
  </head>
  <body>
   <xsl:apply-templates select="tc:collection"/>
  </body>
 </html>
</xsl:template>

<xsl:template match="tc:collection">
 <p id="header-left"><xsl:value-of select="$cdate"/></p>
 <a id="header-right" href="http://lamyseba.github.io/biblioteca">Documentacion</a>
 <h1 class="colltitle">
  <xsl:value-of select="@title"/>
 </h1>

 <table id="myTable" class="display compact">
  <!-- always print headers -->
  <thead>
   <tr>
    <xsl:variable name="fields" select="tc:fields"/>
    <xsl:for-each select="$columns">
     <th>
      <xsl:call-template name="field-title">
       <xsl:with-param name="fields" select="$fields"/>
       <xsl:with-param name="name" select="."/>
      </xsl:call-template>
     </th>
    </xsl:for-each>
   </tr>
  </thead>
  <tbody>
   <xsl:for-each select="tc:entry">
    <!-- Sorting is done case insensitive -->
    <xsl:sort lang="$lang" select="translate(dyn:evaluate($sort1), $lowercase, $uppercase)" data-type="{$sort1-type}"/>
    <xsl:sort lang="$lang" select="translate(dyn:evaluate($sort2), $lowercase, $uppercase)" data-type="{$sort2-type}"/>
    <xsl:sort lang="$lang" select="translate(dyn:evaluate($sort3), $lowercase, $uppercase)" data-type="{$sort3-type}"/>
    <tr class="r{position() mod 2}">
     <xsl:apply-templates select="."/>
    </tr>
   </xsl:for-each>
  </tbody>
 </table>
</xsl:template>

<xsl:template name="field-title">
 <xsl:param name="fields"/>
 <xsl:param name="name"/>
 <!-- remove namespace portion of qname -->
 <xsl:variable name="name-tokens" select="str:tokenize($name, ':')"/>
 <!-- the header is the title attribute of the field node whose
      name equals the column name -->
 <xsl:value-of select="$fields/tc:field[@name = $name-tokens[last()]]/@title"/>
</xsl:template>

<xsl:template match="tc:entry">
 <!-- stick all the descendants into a variable -->
 <xsl:variable name="current" select="descendant::*"/>
 <xsl:variable name="entry" select="."/>

 <xsl:for-each select="$columns">
  <xsl:variable name="column" select="."/>

  <!-- find all descendants whose name matches the column name -->
  <xsl:variable name="numvalues" select="count($current[local-name() = $column])"/>
  <!-- if the field node exists, output its value, otherwise put in a space -->
  <td class="field">
   <xsl:choose>
    <!-- when there is at least one value... -->
    <xsl:when test="$numvalues &gt; 1">
     <xsl:call-template name="simple-field-value">
      <xsl:with-param name="entry" select="$entry"/>
      <xsl:with-param name="field" select="$column"/>
     </xsl:call-template>
    </xsl:when>

    <xsl:when test="$numvalues = 1">
     <xsl:for-each select="$current[local-name() = $column]">

      <xsl:variable name="field" select="key('fieldsByName', $column)"/>
      <xsl:choose>

       <!-- boolean and number values -->
       <xsl:when test="$field/@type=4 or $field/@type=6">
        <xsl:attribute name="style">
         <xsl:text>text-align: center; padding-left: 5px</xsl:text>
        </xsl:attribute>
        <xsl:call-template name="simple-field-value">
         <xsl:with-param name="entry" select="$entry"/>
         <xsl:with-param name="field" select="$column"/>
        </xsl:call-template>
       </xsl:when>

       <!-- next, check for images -->
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

       <!-- if it's a date, format with hyphens -->
       <xsl:when test="$field/@type=12">
        <xsl:attribute name="style">
         <xsl:text>text-align: center; padding-left: 5px</xsl:text>
        </xsl:attribute>
        <xsl:call-template name="simple-field-value">
         <xsl:with-param name="entry" select="$entry"/>
         <xsl:with-param name="field" select="$column"/>
        </xsl:call-template>
       </xsl:when>

       <!-- handle URL here, so no link created -->
       <xsl:when test="$field/@type=7">
        <xsl:value-of select="."/>
       </xsl:when>

       <!-- finally, it's just a regular value -->
       <xsl:otherwise>
        <xsl:call-template name="simple-field-value">
         <xsl:with-param name="entry" select="$entry"/>
         <xsl:with-param name="field" select="$column"/>
        </xsl:call-template>
       </xsl:otherwise>

      </xsl:choose>
     </xsl:for-each>
    </xsl:when>
    <xsl:otherwise>
     <xsl:text> </xsl:text>
    </xsl:otherwise>
   </xsl:choose>
  </td>
 </xsl:for-each>
</xsl:template>

</xsl:stylesheet>
<!-- Local Variables: -->
<!-- sgml-indent-step: 1 -->
<!-- sgml-indent-data: 1 -->
<!-- End: -->
