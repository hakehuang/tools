<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
<xsl:template name="br">
    <xsl:param name="text"/>
    <xsl:choose>
        <xsl:when test="contains($text,'&#xa;')">
            <xsl:value-of select="substring-before($text,'&#xa;')"/>
            <br/>
            <xsl:call-template name="br">
                <xsl:with-param name="text">
                    <xsl:value-of select="substring-after($text,'&#xa;')"/>
                </xsl:with-param>
            </xsl:call-template>
        </xsl:when>
        <xsl:otherwise>
            <xsl:value-of select="$text"/>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>
<xsl:template match="/">
  <html>
  <body>
   <xsl:for-each select="chapter/sect1">
   <div>
   <H2><font color="blue"><xsl:value-of select="title"/></font></H2>
   </div>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th align="left">Attribute</th>
        <th align="left">Value</th>
      </tr>
	<xsl:for-each select="formalpara">
      <tr>
        <td>
		<xsl:value-of select="title"/>
		</td>
        <td>
		<xsl:call-template name="br">
		<xsl:with-param name="text" select="para"/>
		</xsl:call-template>
		<xsl:call-template name="br">
		<xsl:with-param name="text" select="screen"/>
		</xsl:call-template>
		</td>
      </tr>
	</xsl:for-each>
    </table>
	<div>SRS</div>
	<table border="1">
      <tr bgcolor="#9acd32">
        <th align="left">SRSID</th>
        <th align="left">Description</th>
      </tr>
		<xsl:for-each select="sect2/sect3">
      <tr>
        <td>
		<xsl:value-of select="title"/>
		</td>
        <td>
		<xsl:value-of select="formalpara/para"/>
		</td>
      </tr>
		</xsl:for-each>
    </table>
      </xsl:for-each>
  </body>
  </html>
</xsl:template>
</xsl:stylesheet>
