--alla produkter 
SELECT [ProductID],[Name]
FROM [Production].[Product]
ORDER BY [ProductID]

--alla divisioner 
SELECT TerritoryID, [Name],[CountryRegionCode]
FROM [Sales].[SalesTerritory]
ORDER BY TerritoryID

--alla anst�llda
SELECT *
FROM HumanResources.Employee

--alla avdelningar
SELECT [DepartmentID], [Name]
FROM [HumanResources].[Department]
ORDER BY [DepartmentID]

--------------------------------------------------------------------------------------

------1.F�rs�ljningsresultat f�r hela f�retaget

--Totalt f�rs�ljningsresultat i �r j�mf�rt med f�rra �ret
SELECT  
SUM(SalesYTD) AS 'Sales in the year to date',
SUM(SalesLastYear) AS 'Sales in last year'
FROM Sales.SalesTerritory


--Totalt f�rs�ljningsresultat av anst�llda i �r j�mf�rt med f�rra �ret 
SELECT 
SUM(SalesYTD) AS 'SalesYTD', 
SUM(SalesLastYear) AS 'SalesLastYear'
FROM Sales.SalesPerson





----------------------------------------------------------------------------------------

------------------2. F�rs�ljningsresultat i regioner

--F�rs�ljningsresultat per region med tilldelat antal kunder
SELECT A.TerritoryID,
       A.Name, 
       A.CountryRegionCode, 
       A.SalesYTD, 
	   A.SalesLastYear,
	   ChangeYTD= SalesYTD- SalesLastYear, 
	   ChangeYTD_procent=((SalesYTD- SalesLastYear)*100)/SalesLastYear,
	   B.NumberOfCustomer
FROM Sales.SalesTerritory AS A
LEFT JOIN(
SELECT TerritoryID,
COUNT(CustomerID) AS NumberOfCustomer
FROM Sales.Customer 
GROUP BY TerritoryID)AS B ON A. TerritoryID=B.TerritoryID
ORDER BY NumberOfCustomer

--Klarg�randet f�r region 2 och 3

SELECT A.TerritoryID,
       A.Name, 
       A.SalesYTD AS SalesRegYTD, 
	   B.SalesPersonYTD,
	   OnlinesalesYTD=SalesYTD-SalesPersonYTD
FROM Sales.SalesTerritory AS A
LEFT JOIN(
SELECT TerritoryID, 
       SUM(SalesYTD) AS SalesPersonYTD 
FROM Sales.SalesPerson
WHERE TerritoryID IS NOT NULL
GROUP BY TerritoryID) AS B 
ON A.TerritoryID=B.TerritoryID
WHERE A.TerritoryID IN (2, 3)


--m�jlig f�rklaring till det negativa talet av onlinef�rs�ljning i regioner ID=2 och ID=3
SELECT*
FROM Sales.SalesTerritoryHistory
WHERE BusinessEntityID=275 OR BusinessEntityID=277 
ORDER BY BusinessEntityID

--Sammanfattningstabell per region
SELECT A.TerritoryID,
       A.Name, 
       A.SalesYTD AS SalesRegYTD, 
	   B.SalesPersonYTD,
	   Online_salesYTD=SalesYTD-SalesPersonYTD,
	   A.SalesLastYear AS SalesRegLY,
	   B.SalesPersonLY,
	   Online_salesLY=SalesLastYear-SalesPersonLY,
	   ChangeReg=SalesYTD-SalesLastYear,
	   ChangePerson=SalesPersonYTD-SalesPersonLY,
	   ChangeOnline=SalesYTD-SalesPersonYTD

FROM Sales.SalesTerritory AS A
LEFT JOIN(
SELECT TerritoryID, 
       SUM(SalesYTD) AS SalesPersonYTD, 
	   SUM(SalesLastYear) AS SalesPersonLY
FROM Sales.SalesPerson
WHERE TerritoryID is NOT NULL
GROUP BY TerritoryID) AS B 
ON A.TerritoryID=B.TerritoryID
WHERE A.TerritoryID IN (1, 4,5,6,7,8,9,10)
ORDER BY ChangeOnline



------------------------------------------------------------------------------------------------------------------
-------------------------------3. F�rs�ljningsresultat av anst�llda p� f�rs�ljningsavdelningen

--#Alla anst�llda p� f�rs�ljningsavdelningen

SELECT A.BusinessEntityID
	     , B. DepartmentID
		 , B.Name
	   , A.StartDate
	   , A.EndDate
	  FROM HumanResources.EmployeeDepartmentHistory AS A
	  LEFT JOIN(
	  SELECT DepartmentID, Name
	  FROM HumanResources.Department 
	  WHERE DepartmentID=3)
	  AS B ON A.DepartmentID=B.DepartmentID
	  WHERE Name IS NOT NULL
	  ORDER BY Name

--f�rs�ljning av alla anst�llda
SELECT BusinessEntityID,
	  TerritoryID,
	  SalesYTD,
	  SalesLastYear 
	  FROM Sales.SalesPerson

--F�rs�ljning av anst�llda utan region
SELECT A.BusinessEntityID,
	        A.JobTitle,
	        B.TerritoryID,
            B. SalesYTD,
	        B. SalesLastYear 

FROM HumanResources.Employee AS A
INNER JOIN Sales.SalesPerson AS B 
ON A.BusinessEntityID=B.BusinessEntityID
WHERE TerritoryID IS NULL

--F�rs�ljning av anst�llda i regionen
SELECT  A.TerritoryID,
        A.Name,
        B.BusinessEntityID,
        B.SalesYTD,
        B.SalesLastYear,
		B.SalesGrowthYTD
FROM Sales.SalesTerritory AS A
LEFT JOIN(SELECT TerritoryID,
                 BusinessEntityID,
                 SalesYTD,
                 SalesLastYear,
		         SalesGrowthYTD=SalesYTD-SalesLastYear
FROM Sales.SalesPerson ) AS B
ON A.TerritoryID=B.TerritoryID
ORDER BY TerritoryID 

--Anst�llda med negativ f�rs�ljningstillv�xt
SELECT  A.TerritoryID,
        A.Name,
        B.BusinessEntityID,
        B.SalesYTD,
        B.SalesLastYear,
		B.SalesGrowthYTD
FROM Sales.SalesTerritory AS A
LEFT JOIN(SELECT TerritoryID,
                 BusinessEntityID,
                 SalesYTD,
                 SalesLastYear,
		         SalesGrowthYTD=SalesYTD-SalesLastYear
FROM Sales.SalesPerson ) AS B
ON A.TerritoryID=B.TerritoryID
WHERE SalesGrowthYTD<0
ORDER BY SalesGrowthYTD DESC 

--------------------------------------------------------------------------------------------------

---------------------------------4. Konfidensintervall

--ber�kna det totala orderbeloppet f�r varje kund 
SELECT 
CustomerID, 
SUM(SubTotal) AS SaleAmount

FROM Sales.SalesOrderHeader
GROUP BY CustomerID

--30 slumpm�ssigt utvalda kunder
SELECT TOP(30)
CustomerID, 
SUM(SubTotal) AS Amount

FROM Sales.SalesOrderHeader
GROUP BY CustomerID
ORDER BY NEWID()

--1000 slumpm�ssigt utvalda kunder
SELECT TOP(1000)
CustomerID, 
SUM(SubTotal) AS Amount

FROM Sales.SalesOrderHeader
GROUP BY CustomerID
ORDER BY NEWID()
