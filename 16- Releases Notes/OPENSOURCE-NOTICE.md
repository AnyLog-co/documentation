---
title: "Open Source Packages Notice"
description: ""
layout: page
source_path: "release/OPENSOURCE-NOTICE.md"
---
<div id="osn-root" style="--osn-ink:#1c1c1a; --osn-sub:#6b6b64; --osn-line:#dedcd4; --osn-bg:#fffdf9; --osn-row:#f7f5ef; --osn-accent:#3c5a4c; --osn-accent-ink:#fffdf9;">
<style>
  #osn-root {
    font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
    color: var(--osn-ink);
    background: var(--osn-bg);
    padding: 28px 30px 34px;
    border-radius: 10px;
    max-width: 780px;
    margin: 0 auto;
    box-sizing: border-box;
  }
  #osn-root * { box-sizing: border-box; }
  #osn-root h1 {
    font-size: 21px;
    font-weight: 700;
    letter-spacing: -0.01em;
    margin: 0 0 6px;
  }
  #osn-root p.osn-desc {
    font-size: 13.5px;
    line-height: 1.55;
    color: var(--osn-sub);
    margin: 0 0 20px;
    max-width: 62ch;
  }
  .osn-controls {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 14px;
    flex-wrap: wrap;
  }
  .osn-controls span.osn-label {
    font-size: 11.5px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--osn-sub);
    margin-right: 2px;
  }
  .osn-btn {
    font-family: inherit;
    font-size: 13px;
    font-weight: 600;
    color: var(--osn-ink);
    background: var(--osn-row);
    border: 1px solid var(--osn-line);
    border-radius: 7px;
    padding: 6px 12px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: background 0.12s ease, border-color 0.12s ease;
  }
  .osn-btn:hover { border-color: var(--osn-accent); }
  .osn-btn.active {
    background: var(--osn-accent);
    color: var(--osn-accent-ink);
    border-color: var(--osn-accent);
  }
  .osn-btn .osn-arrow {
    font-size: 10px;
    opacity: 0.85;
    transform: translateY(-0.5px);
  }
  .osn-count {
    font-size: 12px;
    color: var(--osn-sub);
    margin-left: auto;
  }
  table.osn-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13.5px;
  }
  .osn-table thead th {
    text-align: left;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--osn-sub);
    font-weight: 600;
    padding: 0 10px 8px;
    border-bottom: 1px solid var(--osn-ink);
  }
  .osn-table tbody tr {
    border-bottom: 1px solid var(--osn-line);
  }
  .osn-table tbody tr:hover { background: var(--osn-row); }
  .osn-table td {
    padding: 9px 10px;
    vertical-align: top;
  }
  .osn-table td.osn-lic {
    color: var(--osn-sub);
    white-space: nowrap;
  }
  .osn-pkg a {
    color: var(--osn-ink);
    text-decoration: none;
    font-weight: 600;
    border-bottom: 1px solid var(--osn-line);
  }
  .osn-pkg a:hover {
    color: var(--osn-accent);
    border-bottom-color: var(--osn-accent);
  }
  .osn-pkg .osn-nolink {
    font-weight: 600;
    color: var(--osn-ink);
  }
  .osn-group-row td {
    padding: 14px 10px 4px;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--osn-accent);
    font-weight: 700;
    border-bottom: none;
  }
  .osn-group-row:first-child td { padding-top: 2px; }
</style>

<h1>Powered by Open-Source Software</h1>
<p class="osn-desc">
  This product incorporates the following third-party open-source Python packages.
  We are grateful to the authors and maintainers of these projects. Package names
  are listed without version numbers, since versions change frequently but the
  license does not. Click a package name to view its PyPI page.
</p>

<div class="osn-controls">
  <span class="osn-label">Sort by</span>
  <button class="osn-btn active" id="osn-sort-name" onclick="osnSort('name')">
    Name <span class="osn-arrow" id="osn-arrow-name">▲</span>
  </button>
  <button class="osn-btn" id="osn-sort-license" onclick="osnSort('license')">
    License <span class="osn-arrow" id="osn-arrow-license">▲</span>
  </button>
  <span class="osn-count" id="osn-count"></span>
</div>

<table class="osn-table">
  <thead>
    <tr><th>Software</th><th>License</th></tr>
  </thead>
  <tbody id="osn-tbody"></tbody>
</table>
</div>

<script>
(function () {
  var data = [
    ["aiofiles", "Apache-2.0", "aiofiles"],
    ["aiohttp", "Apache-2.0", "aiohttp"],
    ["aiosqlite", "MIT", "aiosqlite"],
    ["akave", "Unknown (not on PyPI — appears internal/private)", null],
    ["anthropic", "MIT", "anthropic"],
    ["anyio", "MIT", "anyio"],
    ["av (PyAV)", "BSD-3-Clause", "av"],
    ["boto3", "Apache-2.0", "boto3"],
    ["botocore", "Apache-2.0", "botocore"],
    ["click", "BSD-3-Clause", "click"],
    ["colorama", "BSD-3-Clause", "colorama"],
    ["confluent-kafka", "Apache-2.0", "confluent-kafka"],
    ["cryptography", "Apache-2.0 OR BSD-3-Clause", "cryptography"],
    ["Cython", "Apache-2.0", "Cython"],
    ["distro", "Apache-2.0", "distro"],
    ["dnspython", "ISC", "dnspython"],
    ["docker", "Apache-2.0", "docker"],
    ["docstring_parser", "MIT", "docstring_parser"],
    ["fastapi", "MIT", "fastapi"],
    ["grpcio", "Apache-2.0", "grpcio"],
    ["grpcio-reflection", "Apache-2.0", "grpcio-reflection"],
    ["grpcio-tools", "Apache-2.0", "grpcio-tools"],
    ["httpx", "BSD-3-Clause", "httpx"],
    ["httpx-sse", "MIT", "httpx-sse"],
    ["jaraco.context", "MIT", "jaraco.context"],
    ["jiter", "MIT", "jiter"],
    ["jsonschema", "MIT", "jsonschema"],
    ["jsonschema-specifications", "MIT", "jsonschema-specifications"],
    ["kafka-python", "Apache-2.0", "kafka-python"],
    ["lxml", "BSD-3-Clause", "lxml"],
    ["mcp", "MIT", "mcp"],
    ["mcp-proxy", "MIT", "mcp-proxy"],
    ["netifaces", "MIT", "netifaces"],
    ["Nuitka", "AGPL-3.0-or-later", "Nuitka"],
    ["numpy", "BSD-3-Clause", "numpy"],
    ["opcua", "LGPL-3.0-or-later", "opcua"],
    ["opencv-python-headless", "Apache-2.0", "opencv-python-headless"],
    ["orjson", "Apache-2.0 OR MIT", "orjson"],
    ["paho-mqtt", "EPL-2.0 OR BSD-3-Clause", "paho-mqtt"],
    ["pillow", "MIT-CMU (PIL Software License)", "pillow"],
    ["propcache", "Apache-2.0", "propcache"],
    ["protobuf", "BSD-3-Clause", "protobuf"],
    ["psutil", "BSD-3-Clause", "psutil"],
    ["psycopg2-binary", "LGPL (with exceptions)", "psycopg2-binary"],
    ["py-ecc", "MIT", "py-ecc"],
    ["py4j", "BSD-3-Clause", "py4j"],
    ["pycomm3", "MIT", "pycomm3"],
    ["PyJWT", "MIT", "PyJWT"],
    ["pymodbus", "BSD-3-Clause", "pymodbus"],
    ["pymongo", "Apache-2.0", "pymongo"],
    ["pyOpenSSL", "Apache-2.0", "pyOpenSSL"],
    ["python-dateutil", "Apache-2.0 OR BSD-3-Clause", "python-dateutil"],
    ["python-dotenv", "BSD-3-Clause", "python-dotenv"],
    ["python-multipart", "Apache-2.0", "python-multipart"],
    ["pytz", "MIT", "pytz"],
    ["pywin32", "PSF", "pywin32"],
    ["PyYAML", "MIT", "PyYAML"],
    ["referencing", "MIT", "referencing"],
    ["requests", "Apache-2.0", "requests"],
    ["sortedcontainers", "Apache-2.0", "sortedcontainers"],
    ["sse-starlette", "BSD-3-Clause", "sse-starlette"],
    ["ujson", "BSD-3-Clause AND TCL", "ujson"],
    ["urllib3", "MIT", "urllib3"],
    ["uvicorn", "BSD-3-Clause", "uvicorn"],
    ["web3", "MIT", "web3"],
    ["xhtml2pdf", "Apache-2.0", "xhtml2pdf"],
    ["xmltodict", "MIT", "xmltodict"],
    ["yt-dlp", "Unlicense", "yt-dlp"]
  ];

  var state = { key: "name", dir: 1 };
  var tbody = document.getElementById("osn-tbody");
  document.getElementById("osn-count").textContent = data.length + " packages";

  function escHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function render() {
    var rows = data.slice();
    var key = state.key;
    rows.sort(function (a, b) {
      var av = key === "name" ? a[0].toLowerCase() : a[1].toLowerCase();
      var bv = key === "name" ? b[0].toLowerCase() : b[1].toLowerCase();
      if (av < bv) return -1 * state.dir;
      if (av > bv) return 1 * state.dir;
      return a[0].toLowerCase() < b[0].toLowerCase() ? -1 : 1;
    });

    var html = "";
    if (key === "license") {
      var lastLic = null;
      rows.forEach(function (row) {
        if (row[1] !== lastLic) {
          html += '<tr class="osn-group-row"><td colspan="2">' + escHtml(row[1]) + "</td></tr>";
          lastLic = row[1];
        }
        html += buildRow(row);
      });
    } else {
      rows.forEach(function (row) { html += buildRow(row); });
    }
    tbody.innerHTML = html;

    ["name", "license"].forEach(function (k) {
      var btn = document.getElementById("osn-sort-" + k);
      var arrow = document.getElementById("osn-arrow-" + k);
      var isActive = k === key;
      btn.classList.toggle("active", isActive);
      arrow.textContent = isActive ? (state.dir === 1 ? "▲" : "▼") : "▲";
      arrow.style.visibility = isActive ? "visible" : "hidden";
    });
  }

  function buildRow(row) {
    var name = row[0], lic = row[1], slug = row[2];
    var pkgCell = slug
      ? '<a href="https://pypi.org/project/' + encodeURIComponent(slug) + '/" target="_blank" rel="noopener">' + escHtml(name) + "</a>"
      : '<span class="osn-nolink">' + escHtml(name) + "</span>";
    return "<tr><td class=\"osn-pkg\">" + pkgCell + '</td><td class="osn-lic">' + escHtml(lic) + "</td></tr>";
  }

  window.osnSort = function (key) {
    if (state.key === key) {
      state.dir *= -1;
    } else {
      state.key = key;
      state.dir = 1;
    }
    render();
  };

  render();
})();
</script>|