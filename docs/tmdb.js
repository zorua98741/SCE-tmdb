function generateHash() {
	const shaObj = new jsSHA("SHA-1", "TEXT", {
		hmacKey: {value: "F5DE66D2680E255B2DF79E74F890EBF349262F618BCAE2A9ACCDEE5156CE8DF2CDF2D48C71173CDC2594465B87405D197CF1AED3B7E9671EEB56CA6753C2E6B0", format: "HEX"},
	});
	var titleID = document.getElementById("titleIDText");
	
	let x = titleID.value;
	let y = "_00";
	let input = x.concat(y);
	let inputUpper = input.toUpperCase();
	
	shaObj.update(inputUpper);
	let hmac = shaObj.getHash("HEX");
	let output = hmac.toUpperCase();
	document.getElementById("output").innerHTML = output;
	document.getElementById("input").innerHTML = inputUpper;
}

function generateURL() {
	var pType = document.getElementById("platform").value;
	if (pType == "PS4 (JSON)") {
		var tmdb = "http://tmdb.np.dl.playstation.net/tmdb2/"
		var extension = ".json"
	} else {
		var tmdb = "http://tmdb.np.dl.playstation.net/tmdb/"
		var extension = ".xml"
	}
	var titleID = document.getElementById("input").textContent;
	if (titleID != "___") { 	//stop incomplete link from being generated and shown
		var hash = document.getElementById("output").textContent;
		var genURL = tmdb + titleID + "_" + hash + "/" + titleID + extension;
		document.getElementById("url").innerHTML = genURL;
		document.getElementById("url").href = genURL;
	}
}

function changeTheme() {
	var element = document.body;
	var theme = document.getElementById("theme").value;
	const mode = document.querySelector("#light-mode");
	if (theme == "Light") {
		mode.href = "light-mode.css";
		document.cookie = "theme=light-mode";
	}
	if (theme == "Dark") {
		mode.href = "dark-mode.css";
		document.cookie = "theme=dark-mode";
	}
}

function getCookie() {
	const mode = document.querySelector("#light-mode");
	let decodedCookie = decodeURIComponent(document.cookie);
	console.log(decodedCookie);
	if (decodedCookie == "theme=light-mode") {
		mode.href = "light-mode.css";
		}
	if (decodedCookie == "theme=dark-mode") {
		mode.href = "dark-mode.css";
		}
}
