<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
<xsl:template match="/">
  <html>
  <body>
  	<H1>
		<xsl:value-of select="chapter/title"/>
	</H1>
      <xsl:for-each select="chapter/sect1">
       <div>
	   <H2>
		<xsl:value-of select="title"/>
	   </H2>
		<xsl:for-each select="formalpara">
		 <xsl:if test="not(contains(para, '-'))">
		<p><xsl:value-of select="title"/></p>
		 </xsl:if>
		<p><xsl:value-of select="para"/></p>
      	</xsl:for-each>
	  </div>
      </xsl:for-each>
  </body>
  </html>
</xsl:template>
</xsl:stylesheet>

