Tilde~Tool - IIS shortname enumeration tool
=================================================
By Damien King 
Damien.King@KPMG.co.uk
(c) KPMG LLP

*Please let me know if you find this tool useful*

1 - Background:
	http://soroush.secproject.com/downloadable/microsoft_iis_tilde_character_vulnerability_feature.pdf

2 - Version history:
	1.3.1 
		- Added 'method' switch
		- Output file layout
		- Tidied up code.
		- Other optimisations.
	1.3 
		by AG
		- ~1, ~2 etc cycling
		- differentiating between directories and files
	1.2 - SSL support
	1.1 - Initial release to team for testing

3 - Usage

	tt.py <host> <port> --path <directory to enumerate> --status <status code indicating positive> --method <GET,HEAD,get etc> --output <output filename>
	
	Required params:
		host
			This should start with 'http(s)://...'
		port
			80 or 443 currently accepted.
	
	Optional (but recommended):
		--path
			/path/to/the/target/directory/ to be enumerated.
		--status
			The HTTP status code that indicates a positive hit. This can differ between applications. Could be 401, 404 etc. 
		--method
			Request method used to communicate with target. Use HEAD method to reduce traffic to the target.
		--output
			Name of file to output results to e.g. results.txt.	

	Example:
		tt.py http://192.168.85.130 80 --path / --status 404 --method get --output test.txt


				
Have fun! 




