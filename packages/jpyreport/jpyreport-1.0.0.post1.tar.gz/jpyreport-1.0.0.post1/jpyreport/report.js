function showLevel(level) {
  removeStatusLinkActive();
  var trs = document.getElementsByTagName("tr");
  for (var i = 0; i < trs.length; i++) {
    var tr = trs[i];
    var attr = tr.getAttribute('level');
    show(tr, !attr || attr.split(" ").indexOf(level) > -1);
  }
}

function showStatusLevel(level) {
  var trs = document.getElementsByTagName("tr"), i;
  for (i = 0; i < trs.length; i++) {
    var tr = trs[i];
    var attr = tr.getAttribute('status_level');
    if (attr) {
      show(tr, attr.split(" ").indexOf(level) > -1);
    }
  }

  removeStatusLinkActive(level);
}

function removeStatusLinkActive(except) {
  var statusLinks = document.getElementsByClassName('status_link');
  for (var i = 0; i < statusLinks.length; i++) {
    if (statusLinks[i].classList.contains(except)) {
      statusLinks[i].classList.add('active');
    } else {
      statusLinks[i].classList.remove('active');
    }
  }
}

function show(row, status) {
  if (status) {
    row.classList.remove("hidden");
  } else {
    row.classList.add("hidden");
  }
}

function toggleLevel(level) {
  var trs = getTrsWithLevel(level);
  var hasOpened = false;
  var i;
  for (i = 0; i < trs.length; i++) {
    if (!trs[i].classList.contains("hidden")) {
      hasOpened = true;
    }
  }
  for (i = 0; i < trs.length; i++) {
    show(trs[i], !hasOpened);
  }
}

function getTrsWithLevel(level) {
  var res = [];
  var trs = document.getElementsByTagName("tr");
  for (var i = 0; i < trs.length; i++) {
    var tr = trs[i];
    var attr = tr.getAttribute('level');
    if (attr) {
      var levels = attr.split(" ");
      if (levels.indexOf(level) > -1) {
        res.push(tr);
      }
    }
  }
  return res;
}

function togglePopup(elem) {
  var popup = elem.nextSibling;
  show(popup, popup.classList.contains("hidden"));
}

document.onreadystatechange = function () {
  if (document.readyState === 'complete') {
    showLevel('failed');
  }
};