SET ECHO OFF
 SET pagesize 1000
 set feedback off
 set lines 180

SET MARKUP HTML ON SPOOL ON -
HEAD '<title>My Report</title> -
<style type="text/css"> -
  table {-
        font-family: arial, sans-serif;-
        font-size: 11px;-
        color: #333333;-
        border-width: 1px;-
        border-color: #3A3A3A;-
        border-collapse: collapse;-
    }-
     th {-
        border-width: 1px;-
        padding: 8px;-
        border-style: solid;-
        border-color: #517994;-
        background-color: #B2CFD8;-
    }-
    tr:hover td {-
        background-color: #DFEBF1;-
    }-
   td {-
        border-width: 1px;-
        padding: 8px;-
        border-style: solid;-
        border-color: #517994;-
        background-color: #ffffff;-
    }-
</style>'  body 'text=black bgcolor=fffffff align=left' -
    table 'align=center width=99% border=3 bordercolor=black bgcolor=grey' ENTMAP OFF

    
/* Red Header */
/*
SET MARKUP HTML ON SPOOL ON -
HEAD '<title>My Report</title> -
<style type="text/css"> -
table{-
        font-family: verdana, arial, sans-serif;-
        font-size: 11px;-
        color: #333333;-
        border-width: 1px;-
        border-color: #3A3A3A;-
        border-collapse: collapse;-
    }-
 th {-
        border-width: 1px;-
        padding: 8px;-
        border-style: solid;-
        border-color: #FFA6A6;-
        background-color: #D56A6A;-
        color: #ffffff;-
    }-
 tr:hover td {-
        cursor: pointer;-
        background-color: #F7CFCF;-
    }-
 td {-
        border-width: 1px;-
        padding: 8px;-
        border-style: solid;-
        border-color: #FFA6A6;-
        background-color: #ffffff;-
    }-
</style>' TABLE "border='1' align='left'" ENTMAP OFF
*/

/* Print current date */
COLUMN report_date_col NEW_VALUE report_date
col report_date_col noprint
SELECT TO_CHAR ( SYSDATE ,'DD-Mon-YYYY:HH:MI') AS report_date_col FROM dual;

spool d:\item_mst.html

PROMPT Hi Team,
PROMPT
PROMPT Logon on to OAM (Oracle Applications Manager) and make sure the following processes are running, if not restart them.
PROMPT
PROMPT <h1>Laporan Penjualan per Tanggal</h1> -
       <h3>Tanggal  &report_date </h3> -
       <hr>

column plu noprint 
column plu_external     format a10  heading "PLU External"
column brand            format a20  heading "Brand|Article"
column retail_price     format $999,999  heading "Harga Jual"

select plu,plu_external, brand, retail_price 
from item_mst 
where rownum < 10;

 SPOOL OFF
 SET MARKUP HTML OFF
 exit;