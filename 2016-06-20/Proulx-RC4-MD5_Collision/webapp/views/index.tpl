<!DOCTYPE html>
<html>
	<head>
		<title>MMB's Strawberry Strudel Maker 3000</title>
	</head>
	<body>
		<h1>MMB's Strawberry Strudel Maker 3000</h1>
		<h2>Realtime quality assurance video feed:</h2>
		<img src="static/videofeed.gif">
		
		<!-- Secure management area - `support` can only be enabled by authorized personnel -->
		%if support == 'authorized':
			<div style="display:none;">
				<form action="/upload_new_license_file" method="post" enctype="multipart/form-data">
					<input type="hidden" name="support" value="authorized" />
					<input type="hidden" name="debug" value="false" />
					<input type="file" name="new_license_file" />
					<input type="submit" value="Upload license" />
				</form>
				%if debug == 'true':
					<pre>{{debug_output}}</pre>
				%end
			</div>
		%end
	</body>
</html>