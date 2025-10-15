<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <!-- Output as HTML -->
  <xsl:output method="html" indent="yes"/>

  <xsl:template match="/">
    <html>
      <head>
        <title>988 FM EPG</title>
        <style>
          body { font-family: Arial, sans-serif; background:#f5f5f5; }
          table { border-collapse: collapse; width: 80%; margin: 20px auto; }
          th, td { border: 1px solid #999; padding: 8px; text-align: left; }
          th { background: #222; color: #fff; }
          tr:nth-child(even) { background: #eee; }
        </style>
      </head>
      <body>
        <h2 style="text-align:center;">988 FM EPG</h2>
        <table>
          <tr>
            <th>Start</th>
            <th>Stop</th>
            <th>Title</th>
            <th>Artist</th>
          </tr>
          <xsl:for-each select="tv/programme">
            <tr>
              <td><xsl:value-of select="@start"/></td>
              <td><xsl:value-of select="@stop"/></td>
              <td><xsl:value-of select="title"/></td>
              <td><xsl:value-of select="desc"/></td>
            </tr>
          </xsl:for-each>
        </table>
      </body>
    </html>
  </xsl:template>

</xsl:stylesheet>
