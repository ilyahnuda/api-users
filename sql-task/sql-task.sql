CREATE FUNCTION round_test(fl float) RETURNS integer
	RETURN ceil(fl/5)*5;
-- Task 1
SELECT a.id,
	   a.title, 
	   count(*) as "COUNT" 
	FROM notebooks_brand AS a 
	INNER JOIN notebooks_notebook AS b 
	on a.id = b.brand_id 
 GROUP BY a.id 
 ORDER BY "COUNT" DESC;
-- Task 2
SELECT round_test(width) as width_n,
	   round_test(depth) as depth_n, 
	   round_test(height) as height_n,
	   count(*) as count
	FROM notebooks_notebook
 GROUP BY width_n, depth_n, height_n
 ORDER BY width_n, depth_n, height_n