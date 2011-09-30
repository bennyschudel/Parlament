<?php

if (!is_dir('admin/')) {
	exit('You should run this script from root dir.');
}

$TEMP_DIR = 'admin/images/';
$PARLAMENT_FEED_URL = array(
	'SR' => 'http://www.parlament.ch/d/organe-mitglieder/staenderat/sitzordnung/Seiten/planCE.xml',
	'NR' => 'http://www.parlament.ch/d/organe-mitglieder/nationalrat/sitzordnung/Seiten/planCN.xml',
);
//$PARLIAMENT_PHOTO_URL = 'http://www.parlament.ch/SiteCollectionImages/profil/original/';
$PARLIAMENT_PHOTO_URL = 'http://www.parlament.ch/SiteCollectionImages/profil/gross/';

$panels = array('NR', 'SR');
$pool = array();
$politicians = array();

// load parliament data
foreach($panels as $panel) {
	shell_exec("wget -qO {$TEMP_DIR}{$panel}_feed.xml '{$PARLAMENT_FEED_URL[$panel]}'");
	$file = sprintf('%s%s_feed.xml', $TEMP_DIR, $panel);
	$xml = simplexml_load_file($file);
	foreach ($xml->members->member as $member) {
		$attr = (array)$member->attributes();
		$attr = array_shift($attr);
		$attr['name'] = trim($member);
		$politicians[$attr['bioID']] = array(
			'name'	=> $attr['name'],
			'photo' => $attr['photoID'],
		);
	}
}

file_put_contents("{$TEMP_DIR}politicians.json", json_encode($politicians));

foreach($politicians as $id => $politician) {
	printf("saving {$politician['name']}\n");
	$src = "{$PARLIAMENT_PHOTO_URL}{$politician['photo']}.jpg";
	shell_exec("wget -qO {$TEMP_DIR}/{$id}.jpg '{$src}'");
}

function normalize($text, $delim = ' ', $lower = true) {
		// replace non letter or digits by ' '
	$text = preg_replace('~[^\\pL\d]+~u', $delim, $text);
	$text = trim($text, ' ');
	if (function_exists('iconv')) {
		$text = iconv('utf-8', 'us-ascii//TRANSLIT', $text);
	}
	if ($lower) {
		$text = strtolower($text);
	}
		// remove unwanted characters
	$text = preg_replace('~[^-\s\w]+~', '', $text);

	return $text;
}

function slugify($text) {
	return normalize($text, '-');
}

function match_array($needle, $haystack) {
	$matches = 0;
	foreach ($needle as $item) {
		if (in_array($item, $haystack)) {
			$matches++;
		}
	}

	return ($matches) ? $matches : false;
}

function array_get($array, $key) {
	return $array[$key];
}

