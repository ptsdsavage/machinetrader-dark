#!/usr/bin/env python3
"""
Convert all trading-flows pages from old Webflow theme to new dark Tailwind theme.
Extracts unique content + custom CSS, adapts for dark, wraps in standard template.
"""

import os
import re

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
FLOWS_DIR = os.path.join(WORKSPACE, "trading-flows")

# ── metadata per flow page ──────────────────────────────────────────────
FLOW_META = {
    "bear-call-spread-flow.html": {
        "title": "Bear Call Spread Options Trading Flow | MachineTrader",
        "description": "Automate bearish options trading with the Bear Call Spread strategy. This Node-RED flow executes defined-risk call spreads with position tracking, contract selection, and performance analytics using Alpaca API.",
        "canonical": "https://www.machinetrader.io/trading-flows/bear-call-spread-flow",
        "h1": "Bear Call Spread Options Flow",
        "subtitle": "Generate income in bearish or neutral markets with this credit spread strategy using automated Node-RED trading",
        "badge_text": "📉 Bearish Options Strategy",
        "badge_color": "red-500",
        "gradient_from": "red-500",
        "gradient_to": "orange-500",
        "json_file": "Bear Call Spread (1).json",
    },
    "bear-put-spread-flow.html": {
        "title": "Bear Put Spread Options Trading Flow | MachineTrader",
        "description": "Automate bearish options trading with the Bear Put Spread strategy. This Node-RED flow executes defined-risk put spreads on XLK with position tracking, contract selection, and performance analytics.",
        "canonical": "https://www.machinetrader.io/trading-flows/bear-put-spread-flow",
        "h1": "Bear Put Spread Options Flow",
        "subtitle": "Profit from bearish moves with defined-risk put spreads using automated Node-RED trading",
        "badge_text": "📉 Bearish Options Strategy",
        "badge_color": "red-500",
        "gradient_from": "red-500",
        "gradient_to": "purple-500",
        "json_file": "Bear Put Spread (1).json",
    },
    "bitcoin-etf-portfolio-flow.html": {
        "title": "Bitcoin ETF Portfolio Trading Flow | MachineTrader",
        "description": "Create and manage a diversified Bitcoin ETF portfolio with this automated Node-RED trading flow. Includes buy, sell, and performance tracking for 11 Bitcoin ETFs.",
        "canonical": "https://www.machinetrader.io/trading-flows/bitcoin-etf-portfolio-flow",
        "h1": "Bitcoin ETF Portfolio Trading Flow",
        "subtitle": "Automate a diversified Bitcoin ETF portfolio with buy, sell, and performance tracking for 11 Bitcoin ETFs",
        "badge_text": "₿ Crypto Portfolio",
        "badge_color": "amber-500",
        "gradient_from": "amber-500",
        "gradient_to": "yellow-400",
        "json_file": "Create Bitcoin ETF Portfolio.json",
    },
    "crypto-portfolio-flow.html": {
        "title": "Crypto Portfolio Trading Flow | MachineTrader",
        "description": "Create and manage a diversified cryptocurrency portfolio with this automated Node-RED trading flow. Includes buy, sell, and performance tracking for 17 crypto assets.",
        "canonical": "https://www.machinetrader.io/trading-flows/crypto-portfolio-flow",
        "h1": "Crypto Portfolio Trading Flow",
        "subtitle": "Build and manage a diversified cryptocurrency portfolio with automated buy, sell, and performance tracking",
        "badge_text": "🪙 Crypto Portfolio",
        "badge_color": "purple-500",
        "gradient_from": "purple-500",
        "gradient_to": "indigo-400",
        "json_file": "Create Crypto Portfolio.json",
    },
    "faang-portfolio-flow.html": {
        "title": "FAANG Portfolio Trading Flow | MachineTrader",
        "description": "Create and manage a diversified FAANG stock portfolio with this automated Node-RED trading flow. Includes buy, sell, and performance tracking.",
        "canonical": "https://www.machinetrader.io/trading-flows/faang-portfolio-flow",
        "h1": "FAANG Portfolio Trading Flow",
        "subtitle": "Automate a FAANG stock portfolio with position management, rebalancing, and performance tracking",
        "badge_text": "📊 Equity Portfolio",
        "badge_color": "blue-500",
        "gradient_from": "blue-500",
        "gradient_to": "cyan-400",
        "json_file": "Create FAANG Portfolio.json",
    },
}


def extract_custom_css(content):
    """Extract the <style> block and adapt colours for dark theme."""
    style_match = re.search(r"<style>(.*?)</style>", content, re.DOTALL)
    if not style_match:
        return ""
    css = style_match.group(1)

    # ── light → dark colour swaps ──
    # feature-card, stat-card, step-card, instructions-list backgrounds
    css = css.replace("background: white;", "background: rgba(255,255,255,0.04);")
    css = css.replace("background: #f8fafc;", "background: rgba(255,255,255,0.04);")
    css = re.sub(
        r"background: linear-gradient\(135deg, #f8fafc 0%, #f1f5f9 100%\);",
        "background: rgba(255,255,255,0.04);",
        css,
    )
    css = re.sub(
        r"background: linear-gradient\(135deg, #f1f5f9 0%, #f8fafc 100%\);",
        "background: rgba(255,255,255,0.04);",
        css,
    )

    # text colours
    css = css.replace("color: #1e1e2e;", "color: #f1f5f9;")
    css = css.replace("color: #1e293b;", "color: #f1f5f9;")
    css = css.replace("color: #333;", "color: #e5e7eb;")
    css = css.replace("color: #666;", "color: #9ca3af;")
    css = css.replace("color: #475569;", "color: #9ca3af;")

    # box shadows – lighten for dark
    css = re.sub(
        r"box-shadow: 0 4px 20px rgba\(0, 0, 0, 0\.08\);",
        "box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);",
        css,
    )
    css = re.sub(
        r"box-shadow: 0 10px 40px rgba\(0, 0, 0, 0\.3\);",
        "box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);",
        css,
    )

    # borders
    css = css.replace("border-bottom: 1px solid #e2e8f0;", "border-bottom: 1px solid rgba(255,255,255,0.08);")
    css = css.replace("border: 1px solid #e2e8f0;", "border: 1px solid rgba(255,255,255,0.08);")

    # warning / info / profit / risk boxes → translucent dark versions
    css = re.sub(
        r"background: linear-gradient\(135deg, #fef3c7 0%, #fde68a 100%\);",
        "background: rgba(245,158,11,0.08);",
        css,
    )
    css = css.replace("color: #92400e;", "color: #fbbf24;")

    css = re.sub(
        r"background: linear-gradient\(135deg, #dbeafe 0%, #bfdbfe 100%\);",
        "background: rgba(59,130,246,0.08);",
        css,
    )
    css = css.replace("color: #1e40af;", "color: #93c5fd;")

    css = re.sub(
        r"background: linear-gradient\(135deg, #d1fae5 0%, #a7f3d0 100%\);",
        "background: rgba(16,185,129,0.08);",
        css,
    )
    css = css.replace("color: #065f46;", "color: #6ee7b7;")

    css = re.sub(
        r"background: linear-gradient\(135deg, #fce7f3 0%, #fbcfe8 100%\);",
        "background: rgba(236,72,153,0.08);",
        css,
    )
    css = css.replace("color: #9d174d;", "color: #f9a8d4;")

    # section divider
    css = re.sub(
        r"background: linear-gradient\(90deg, transparent, #e2e8f0, transparent\);",
        "background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);",
        css,
    )

    # comparison table
    css = css.replace("background: white;", "background: rgba(255,255,255,0.04);")
    css = re.sub(
        r"(\.comparison-table td\s*\{[^}]*?)background:\s*white;",
        r"\1background: rgba(255,255,255,0.02);",
        css,
    )

    # crypto / etf tables
    css = re.sub(
        r"(\.crypto-table td\s*\{[^}]*?)background:\s*[^;]+;",
        r"\1background: rgba(255,255,255,0.02);",
        css,
    )
    css = re.sub(
        r"(\.etf-table td\s*\{[^}]*?)background:\s*[^;]+;",
        r"\1background: rgba(255,255,255,0.02);",
        css,
    )

    return css


def extract_main_content(content):
    """Extract main content between header section and footer.

    The pages follow this structure:
      ... PAGE HEADER ... </div> </div> </div>
      <!-- MAIN CONTENT SECTION -->
      <div class="section-learn-main" id="features">
        ... all the real content ...
      </div>
      <!-- FOOTER -->
    We grab from MAIN CONTENT to before the FOOTER.
    """
    # Try to find start of main content
    start_markers = [
        '<!-- MAIN CONTENT SECTION -->',
        'id="features"',
        '<div class="section-learn-main"',
    ]
    start_idx = -1
    for marker in start_markers:
        idx = content.find(marker)
        if idx != -1:
            start_idx = idx
            break

    if start_idx == -1:
        # Fallback: find first main-heading_blacl
        idx = content.find('class="main-heading_blacl"')
        if idx != -1:
            # Walk back to find containing div
            start_idx = content.rfind("<div", 0, idx)

    # Find end: before footer
    end_markers = [
        '<!-- FOOTER -->',
        '<!-- ============================================ -->\n<!-- FOOTER',
        '<div class="footer">',
        '<footer',
    ]
    end_idx = len(content)
    for marker in end_markers:
        idx = content.find(marker)
        if idx != -1 and idx > start_idx:
            end_idx = idx
            break

    main_html = content[start_idx:end_idx]

    # Strip the outer Webflow container wrappers, keep inner content
    # Remove section-learn-main wrapper
    main_html = re.sub(
        r'<div class="section-learn-main"[^>]*>\s*<div class="w-container">\s*',
        '',
        main_html,
        count=1,
    )
    # Remove the comment line
    main_html = re.sub(r'<!-- ={2,} -->\s*', '', main_html)
    main_html = re.sub(r'<!-- MAIN CONTENT SECTION -->\s*', '', main_html)

    # Remove trailing closing divs from the container wrappers
    # (2 closing divs for section-learn-main + w-container)
    main_html = main_html.rstrip()
    if main_html.endswith("</div>"):
        main_html = main_html[:-6].rstrip()
    if main_html.endswith("</div>"):
        main_html = main_html[:-6].rstrip()

    # Adapt Webflow layout classes to Tailwind
    # w-row → grid / flex
    main_html = re.sub(r'class="columns-4 w-row"', 'class="mb-8"', main_html)
    main_html = re.sub(r'class="w-row"', 'class="grid grid-cols-1 md:grid-cols-2 gap-6"', main_html)
    main_html = re.sub(r'class="w-col w-col-12"', 'class="col-span-full"', main_html)
    main_html = re.sub(r'class="w-col w-col-6"', 'class=""', main_html)
    main_html = re.sub(r'class="w-col w-col-4"', 'class=""', main_html)

    # Headings
    main_html = re.sub(
        r'<h2 class="main-heading_blacl"[^>]*>',
        '<h2 class="text-2xl font-bold text-white mb-4">',
        main_html,
    )

    # Fix internal links
    main_html = re.sub(r'href="/trading-flows"', 'href="index.html"', main_html)
    main_html = re.sub(r'href="../index.html#pricing"', 'href="../index.html#pricing"', main_html)  # keep absolute
    main_html = re.sub(r'href="/data-center"', 'href="../data-center.html"', main_html)
    main_html = re.sub(r'href="/learn"', 'href="../learn.html"', main_html)

    return main_html


def generate_dark_flow_page(filename, meta, custom_css, main_content):
    """Generate the full dark-theme page for a trading-flow."""

    json_file = meta.get("json_file", "")
    # Build the JSON loading script if there's a json_file
    json_script = ""
    if json_file:
        json_script = f"""
    // Load the JSON file dynamically
    fetch('{json_file}')
      .then(r => r.ok ? r.text() : Promise.reject('File not found'))
      .then(data => {{
        try {{
          const jsonObj = JSON.parse(data);
          document.getElementById('jsonCode').textContent = JSON.stringify(jsonObj, null, 2);
        }} catch (e) {{
          document.getElementById('jsonCode').textContent = data;
        }}
      }})
      .catch(err => {{
        const el = document.getElementById('jsonCode');
        if (el) el.textContent = 'Error loading JSON file. Please download directly using the link below.';
      }});"""

    return f'''<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{meta["title"]}</title>
  <link rel="canonical" href="{meta["canonical"]}" />
  <meta name="description" content="{meta["description"]}" />
  <meta property="og:title" content="{meta["title"]}" />
  <meta property="og:description" content="{meta["description"]}" />
  <meta property="og:type" content="website" />
  <meta property="twitter:title" content="{meta["title"]}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="google-site-verification" content="google6132bb2f08408978.html" />
  <link rel="icon" href="../images/favicon.svg" type="image/svg+xml" />
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet" />
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{ sans: ['Inter', 'system-ui', 'sans-serif'] }},
          colors: {{
            brand: {{ 50:'#fff8f0',100:'#ffe8cc',200:'#ffd199',300:'#ffb366',400:'#ff9533',500:'#ff6b00',600:'#e05e00',700:'#b84d00',800:'#8f3c00',900:'#662b00',950:'#3d1a00' }},
            accent: {{ 500:'#489fd9',600:'#3a87be' }},
            mt: {{ green:'#4dbd90',purple:'#8668ab',blue:'#489fd9',pink:'#fde5e5',lavender:'#dde7ed' }},
            dark: {{ 900:'#0a0f1a',800:'#111827',700:'#1f2937',600:'#374151' }}
          }}
        }}
      }}
    }}
  </script>
  <link rel="stylesheet" href="../css/styles.css" />
  <!-- Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-G9L6L77LNM"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('set','developer_id.dZGVlNj',true);gtag('js',new Date());gtag('config','G-G9L6L77LNM');</script>
  <script>!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','1830322441099552');fbq('track','PageView');</script>
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','GTM-5DGHXVQ');</script>
  <style>
{custom_css}
  </style>
</head>
<body class="bg-black text-gray-100 font-sans antialiased">

  <!-- ============ PASSWORD GATE ============ -->
  <div id="lock-screen" class="fixed inset-0 z-[9999] bg-black flex items-center justify-center">
    <div class="w-full max-w-sm mx-auto px-6">
      <div class="text-center mb-8">
        <img src="../images/logo.svg" alt="MachineTrader" class="h-12 w-auto mx-auto mb-4" />
        <h1 class="text-2xl font-bold tracking-tight mb-2 text-white">MachineTrader\u2122</h1>
        <p class="text-gray-400 text-sm">Enter the password to view this page.</p>
      </div>
      <form id="password-form" class="space-y-4">
        <div class="relative">
          <input id="password-input" type="password" placeholder="Password" autocomplete="off"
            class="w-full px-4 py-3 rounded-xl bg-gray-900 border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition text-sm" />
        </div>
        <button type="submit" class="btn-primary w-full text-sm font-semibold px-6 py-3 rounded-xl">Enter</button>
        <p id="password-error" class="text-red-500 text-xs text-center hidden">Incorrect password. Try again.</p>
      </form>
    </div>
  </div>

  <!-- ============ PAGE CONTENT ============ -->
  <div id="page-content" class="hidden">

  <!-- ============ NAVIGATION ============ -->
  <nav id="navbar" class="fixed top-0 left-0 right-0 z-50 transition-all duration-300">
    <div class="max-w-7xl mx-auto px-6 lg:px-8">
      <div class="flex items-center justify-between h-20">
        <a href="../index.html" class="flex items-center gap-3 group">
          <img src="../images/logo.svg" alt="MachineTrader" class="h-9 w-auto" />
          <span class="text-xl font-bold tracking-tight text-white">MachineTrader\u2122</span>
        </a>
        <div class="hidden lg:flex items-center gap-8">
          <a href="../index.html" class="nav-link text-sm font-medium text-gray-400 hover:text-white transition">Home</a>
          <a href="../features.html" class="nav-link text-sm font-medium text-gray-400 hover:text-white transition">Features</a>
          <a href="../learn.html" class="nav-link text-sm font-medium text-gray-400 hover:text-white transition">Learn</a>
          <a href="../data-center.html" class="nav-link text-sm font-medium text-gray-400 hover:text-white transition">Data Center</a>
          <a href="../index.html#pricing" class="btn-primary text-sm font-semibold px-6 py-2.5 rounded-full">Start Free Trial</a>
        </div>
        <button id="mobile-menu-btn" class="lg:hidden flex flex-col gap-1.5 p-2" aria-label="Toggle menu">
          <span class="hamburger-line w-6 h-0.5 bg-white rounded transition-all"></span>
          <span class="hamburger-line w-6 h-0.5 bg-white rounded transition-all"></span>
          <span class="hamburger-line w-6 h-0.5 bg-white rounded transition-all"></span>
        </button>
      </div>
    </div>
    <div id="mobile-menu" class="lg:hidden hidden bg-black/95 backdrop-blur-xl border-t border-white/10">
      <div class="max-w-7xl mx-auto px-6 py-6 flex flex-col gap-4">
        <a href="../index.html" class="mobile-nav-link text-base font-medium text-gray-400 hover:text-white py-2">Home</a>
        <a href="../features.html" class="mobile-nav-link text-base font-medium text-gray-400 hover:text-white py-2">Features</a>
        <a href="../learn.html" class="mobile-nav-link text-base font-medium text-gray-400 hover:text-white py-2">Learn</a>
        <a href="../data-center.html" class="mobile-nav-link text-base font-medium text-gray-400 hover:text-white py-2">Data Center</a>
        <div class="flex flex-col gap-3 pt-4 border-t border-white/10">
          <a href="../index.html#pricing" class="btn-primary text-center text-base font-semibold px-6 py-3 rounded-full">Start Free Trial</a>
        </div>
      </div>
    </div>
  </nav>

  <!-- ============ HERO ============ -->
  <section class="relative pt-32 pb-16 overflow-hidden">
    <div class="absolute top-20 left-1/4 w-[500px] h-[500px] bg-{meta["gradient_from"]}/10 rounded-full blur-[120px] pointer-events-none"></div>
    <div class="absolute bottom-0 right-1/4 w-[400px] h-[400px] bg-{meta["gradient_to"]}/10 rounded-full blur-[100px] pointer-events-none"></div>
    <div class="relative max-w-7xl mx-auto px-6 lg:px-8 text-center">
      <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-{meta["badge_color"]}/10 border border-{meta["badge_color"]}/20 text-{meta["badge_color"]} text-sm font-medium mb-8">
        {meta["badge_text"]}
      </div>
      <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight mb-6">
        <span class="text-white">{meta["h1"]}</span>
      </h1>
      <p class="text-lg text-gray-400 max-w-2xl mx-auto mb-6">{meta["subtitle"]}</p>
      <a href="#flow-json" class="btn-primary text-sm font-semibold px-8 py-3 rounded-full inline-flex items-center gap-2">
        View Flow JSON
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"/></svg>
      </a>
    </div>
  </section>

  <!-- ============ MAIN CONTENT ============ -->
  <section class="border-t border-white/5">
    <div class="max-w-5xl mx-auto px-6 lg:px-8 py-16">
{main_content}
    </div>
  </section>

  <!-- ============ CTA ============ -->
  <section class="border-t border-white/5 py-24 text-center">
    <div class="max-w-3xl mx-auto px-6">
      <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight mb-6 text-white">Ready to Automate Your Trading?</h2>
      <p class="text-gray-400 text-lg mb-10">Import this flow into your MachineTrader\u2122 instance and start trading automatically.</p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <a href="../index.html#pricing" class="btn-primary text-lg font-semibold px-10 py-4 rounded-full inline-flex items-center gap-2">
          Start Free Trial
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
        </a>
        <a href="index.html" class="text-lg font-semibold px-10 py-4 rounded-full border border-white/20 text-white hover:bg-white/5 transition inline-flex items-center gap-2">
          All Trading Flows
        </a>
      </div>
    </div>
  </section>

  <!-- ============ FOOTER ============ -->
  <footer class="bg-gray-950 border-t border-white/10">
    <div class="max-w-7xl mx-auto px-6 lg:px-8 py-16">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-10 mb-16">
        <div class="col-span-2 md:col-span-1">
          <a href="../index.html" class="flex items-center gap-2 mb-4">
            <img src="../images/logo.svg" alt="MachineTrader" class="h-8 w-auto" />
            <span class="text-lg font-bold text-white">MachineTrader\u2122</span>
          </a>
          <p class="text-sm text-gray-500 leading-relaxed">Automate your trading strategies using our low-code/no-code MachineTrader\u2122 software.</p>
        </div>
        <div>
          <h4 class="text-sm font-semibold text-brand-500 uppercase mb-4">Product</h4>
          <ul class="space-y-3 text-sm text-gray-500">
            <li><a href="../features.html" class="hover:text-white transition">Features</a></li>
            <li><a href="../index.html#pricing" class="hover:text-white transition">Pricing</a></li>
            <li><a href="../data-center.html" class="hover:text-white transition">Data Center</a></li>
            <li><a href="index.html" class="hover:text-white transition">Trading Scripts</a></li>
            <li><a href="../backtests.html" class="hover:text-white transition">Backtests</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-sm font-semibold text-brand-500 uppercase mb-4">Resources</h4>
          <ul class="space-y-3 text-sm text-gray-500">
            <li><a href="../about-us.html" class="hover:text-white transition">About Us</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-sm font-semibold text-brand-500 uppercase mb-4">Legal</h4>
          <ul class="space-y-3 text-sm text-gray-500">
            <li><a href="../privacy-policy.html" class="hover:text-white transition">Privacy Policy</a></li>
            <li><a href="../terms-of-service.html" class="hover:text-white transition">Terms of Service</a></li>
            <li><a href="../cookie-policy.html" class="hover:text-white transition">Cookie Policy</a></li>
          </ul>
        </div>
      </div>
      <div class="border-t border-white/10 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
        <div class="text-sm text-gray-500">\u00a9 2022\u20132026 MachineTrader\u2122. All Rights Reserved. \u00b7 30 Wall Street, 8th Floor, New York, NY 10005</div>
        <div class="flex items-center gap-6">
          <a href="mailto:info@machinetrader.io" class="text-gray-500 hover:text-white transition text-sm">info@machinetrader.io</a>
        </div>
      </div>
    </div>
    <div class="bg-black border-t border-white/5">
      <div class="max-w-7xl mx-auto px-6 lg:px-8 py-6">
        <p class="text-xs text-gray-600 leading-relaxed">
          <strong class="text-gray-500">Disclaimer:</strong> MachineTrader provides technology for automated trading. All trading involves risk. Past performance is not indicative of future results. MachineTrader is not a registered broker-dealer or investment advisor. Securities trading is offered through Alpaca Securities LLC, member FINRA/SIPC. *Commission-free for U.S. equities.
        </p>
      </div>
    </div>
  </footer>

  </div><!-- end #page-content -->

  <!-- ============ SCRIPTS ============ -->
  <script>
    const EXPECTED_HASH = '8b32a1ee1c55f72d3dd33bdc6cc54b873d7307fe1972855b1cb2d2d11181222f';
    async function sha256(message) {{
      const msgBuffer = new TextEncoder().encode(message);
      const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
      const hashArray = Array.from(new Uint8Array(hashBuffer));
      return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }}
    (async () => {{
      const lockScreen = document.getElementById('lock-screen');
      const pageContent = document.getElementById('page-content');
      const form = document.getElementById('password-form');
      const input = document.getElementById('password-input');
      const error = document.getElementById('password-error');
      if (sessionStorage.getItem('mt-auth') === EXPECTED_HASH) {{
        lockScreen.classList.add('hidden');
        pageContent.classList.remove('hidden');
      }} else {{ input.focus(); }}
      form.addEventListener('submit', async (e) => {{
        e.preventDefault();
        const hash = await sha256(input.value);
        if (hash === EXPECTED_HASH) {{
          sessionStorage.setItem('mt-auth', EXPECTED_HASH);
          lockScreen.style.transition = 'opacity 0.4s ease';
          lockScreen.style.opacity = '0';
          setTimeout(() => {{ lockScreen.classList.add('hidden'); pageContent.classList.remove('hidden'); }}, 400);
        }} else {{
          error.classList.remove('hidden'); input.classList.add('!border-red-500'); input.value = ''; input.focus();
          setTimeout(() => {{ error.classList.add('hidden'); input.classList.remove('!border-red-500'); }}, 3000);
        }}
      }});
    }})();
    {json_script}
    // Copy to clipboard function
    function copyCode() {{
      const codeElement = document.getElementById('jsonCode');
      if (!codeElement) return;
      navigator.clipboard.writeText(codeElement.textContent).then(() => {{
        const btn = document.querySelector('.copy-button');
        const txt = document.getElementById('copyText');
        if (btn) btn.classList.add('copied');
        if (txt) txt.textContent = 'Copied!';
        setTimeout(() => {{
          if (btn) btn.classList.remove('copied');
          if (txt) txt.textContent = 'Copy to Clipboard';
        }}, 2000);
      }}).catch(err => console.error('Copy failed:', err));
    }}
  </script>
  <script src="../js/main.js"></script>
</body>
</html>'''


def generate_index_page():
    """Generate the dark-theme trading-flows/index.html."""
    flows = [
        ("bear-call-spread-flow.html", "Bear Call Spread", "📉", "Bearish credit spread using call options", "red-500"),
        ("bear-put-spread-flow.html", "Bear Put Spread", "📉", "Bearish debit spread using put options", "red-500"),
        ("bitcoin-etf-portfolio-flow.html", "Bitcoin ETF Portfolio", "₿", "Diversified portfolio of 11 Bitcoin ETFs", "amber-500"),
        ("crypto-portfolio-flow.html", "Crypto Portfolio", "🪙", "Portfolio of 17 cryptocurrency assets", "purple-500"),
        ("faang-portfolio-flow.html", "FAANG Portfolio", "📊", "Portfolio of major tech stocks", "blue-500"),
    ]

    cards_html = ""
    for href, name, emoji, desc, color in flows:
        cards_html += f"""
              <a href="{href}" class="group bg-gray-900/40 border border-white/10 rounded-xl p-6 hover:border-{color}/40 hover:bg-{color}/5 transition-all">
                <div class="flex items-center gap-3 mb-3">
                  <div class="w-12 h-12 rounded-lg bg-{color}/10 flex items-center justify-center text-2xl">{emoji}</div>
                  <h3 class="text-base font-semibold text-white group-hover:text-{color} transition">{name}</h3>
                </div>
                <p class="text-sm text-gray-500">{desc}</p>
              </a>
"""

    return f'''<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Trading Scripts &amp; Flows | MachineTrader</title>
  <link rel="canonical" href="https://www.machinetrader.io/trading-flows" />
  <meta name="description" content="Explore trading scripts and automated trading flows on MachineTrader. Build your own algorithmic trading strategies without code." />
  <meta property="og:title" content="Trading Scripts & Flows | MachineTrader" />
  <meta property="og:description" content="Explore trading scripts and automated trading flows on MachineTrader." />
  <meta property="og:type" content="website" />
  <meta property="twitter:title" content="Trading Scripts & Flows | MachineTrader" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="google-site-verification" content="google6132bb2f08408978.html" />
  <link rel="icon" href="../images/favicon.svg" type="image/svg+xml" />
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet" />
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{ sans: ['Inter', 'system-ui', 'sans-serif'] }},
          colors: {{
            brand: {{ 50:'#fff8f0',100:'#ffe8cc',200:'#ffd199',300:'#ffb366',400:'#ff9533',500:'#ff6b00',600:'#e05e00',700:'#b84d00',800:'#8f3c00',900:'#662b00',950:'#3d1a00' }},
            accent: {{ 500:'#489fd9',600:'#3a87be' }},
            mt: {{ green:'#4dbd90',purple:'#8668ab',blue:'#489fd9',pink:'#fde5e5',lavender:'#dde7ed' }},
            dark: {{ 900:'#0a0f1a',800:'#111827',700:'#1f2937',600:'#374151' }}
          }}
        }}
      }}
    }}
  </script>
  <link rel="stylesheet" href="../css/styles.css" />
  <!-- Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-G9L6L77LNM"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('set','developer_id.dZGVlNj',true);gtag('js',new Date());gtag('config','G-G9L6L77LNM');</script>
  <script>!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','1830322441099552');fbq('track','PageView');</script>
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','GTM-5DGHXVQ');</script>
</head>
<body class="bg-black text-gray-100 font-sans antialiased">

  <!-- ============ PASSWORD GATE ============ -->
  <div id="lock-screen" class="fixed inset-0 z-[9999] bg-black flex items-center justify-center">
    <div class="w-full max-w-sm mx-auto px-6">
      <div class="text-center mb-8">
        <img src="../images/logo.svg" alt="MachineTrader" class="h-12 w-auto mx-auto mb-4" />
        <h1 class="text-2xl font-bold tracking-tight mb-2 text-white">MachineTrader\u2122</h1>
        <p class="text-gray-400 text-sm">Enter the password to view this page.</p>
      </div>
      <form id="password-form" class="space-y-4">
        <div class="relative">
          <input id="password-input" type="password" placeholder="Password" autocomplete="off"
            class="w-full px-4 py-3 rounded-xl bg-gray-900 border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition text-sm" />
        </div>
        <button type="submit" class="btn-primary w-full text-sm font-semibold px-6 py-3 rounded-xl">Enter</button>
        <p id="password-error" class="text-red-500 text-xs text-center hidden">Incorrect password. Try again.</p>
      </form>
    </div>
  </div>

  <!-- ============ PAGE CONTENT ============ -->
  <div id="page-content" class="hidden">

  <!-- ============ NAVIGATION ============ -->
  <nav id="navbar" class="fixed top-0 left-0 right-0 z-50 transition-all duration-300">
    <div class="max-w-7xl mx-auto px-6 lg:px-8">
      <div class="flex items-center justify-between h-20">
        <a href="../index.html" class="flex items-center gap-3 group">
          <img src="../images/logo.svg" alt="MachineTrader" class="h-9 w-auto" />
          <span class="text-xl font-bold tracking-tight text-white">MachineTrader\u2122</span>
        </a>
        <div class="hidden lg:flex items-center gap-8">
          <a href="../index.html" class="nav-link text-sm font-medium text-gray-400 hover:text-white transition">Home</a>
          <a href="../features.html" class="nav-link text-sm font-medium text-gray-400 hover:text-white transition">Features</a>
          <a href="../learn.html" class="nav-link text-sm font-medium text-gray-400 hover:text-white transition">Learn</a>
          <a href="../data-center.html" class="nav-link text-sm font-medium text-gray-400 hover:text-white transition">Data Center</a>
          <a href="../index.html#pricing" class="btn-primary text-sm font-semibold px-6 py-2.5 rounded-full">Start Free Trial</a>
        </div>
        <button id="mobile-menu-btn" class="lg:hidden flex flex-col gap-1.5 p-2" aria-label="Toggle menu">
          <span class="hamburger-line w-6 h-0.5 bg-white rounded transition-all"></span>
          <span class="hamburger-line w-6 h-0.5 bg-white rounded transition-all"></span>
          <span class="hamburger-line w-6 h-0.5 bg-white rounded transition-all"></span>
        </button>
      </div>
    </div>
    <div id="mobile-menu" class="lg:hidden hidden bg-black/95 backdrop-blur-xl border-t border-white/10">
      <div class="max-w-7xl mx-auto px-6 py-6 flex flex-col gap-4">
        <a href="../index.html" class="mobile-nav-link text-base font-medium text-gray-400 hover:text-white py-2">Home</a>
        <a href="../features.html" class="mobile-nav-link text-base font-medium text-gray-400 hover:text-white py-2">Features</a>
        <a href="../learn.html" class="mobile-nav-link text-base font-medium text-gray-400 hover:text-white py-2">Learn</a>
        <a href="../data-center.html" class="mobile-nav-link text-base font-medium text-gray-400 hover:text-white py-2">Data Center</a>
        <div class="flex flex-col gap-3 pt-4 border-t border-white/10">
          <a href="../index.html#pricing" class="btn-primary text-center text-base font-semibold px-6 py-3 rounded-full">Start Free Trial</a>
        </div>
      </div>
    </div>
  </nav>

  <!-- ============ HERO ============ -->
  <section class="relative pt-32 pb-16 overflow-hidden">
    <div class="absolute top-20 left-1/4 w-[500px] h-[500px] bg-brand-500/10 rounded-full blur-[120px] pointer-events-none"></div>
    <div class="absolute bottom-0 right-1/4 w-[400px] h-[400px] bg-mt-purple/10 rounded-full blur-[100px] pointer-events-none"></div>
    <div class="relative max-w-7xl mx-auto px-6 lg:px-8 text-center">
      <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-500 text-sm font-medium mb-8">
        <span>\u26a1</span> Automated Trading Flows
      </div>
      <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight mb-6">
        <span class="text-white">Trading Scripts</span>
        <br />
        <span class="bg-gradient-to-r from-brand-500 to-mt-purple bg-clip-text text-transparent">&amp; Flows</span>
      </h1>
      <p class="text-lg text-gray-400 max-w-2xl mx-auto">Ready-to-import Node-RED flows for automated trading. Copy the JSON, import into your MachineTrader\u2122 instance, and start trading.</p>
    </div>
  </section>

  <!-- ============ FLOWS GRID ============ -->
  <section class="border-t border-white/5">
    <div class="max-w-5xl mx-auto px-6 lg:px-8 py-16">

      <h2 class="text-2xl font-bold text-white mb-3">Options Strategies</h2>
      <p class="text-gray-400 mb-8">Defined-risk options spreads with automated execution, position tracking, and P&L analytics.</p>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-16">
        <a href="bear-call-spread-flow.html" class="group bg-gray-900/40 border border-white/10 rounded-xl p-6 hover:border-red-500/40 hover:bg-red-500/5 transition-all">
          <div class="flex items-center gap-3 mb-3">
            <div class="w-12 h-12 rounded-lg bg-red-500/10 flex items-center justify-center text-2xl">\U0001f4c9</div>
            <h3 class="text-base font-semibold text-white group-hover:text-red-500 transition">Bear Call Spread</h3>
          </div>
          <p class="text-sm text-gray-500">Bearish credit spread using call options with automated contract selection and performance tracking.</p>
        </a>
        <a href="bear-put-spread-flow.html" class="group bg-gray-900/40 border border-white/10 rounded-xl p-6 hover:border-red-500/40 hover:bg-red-500/5 transition-all">
          <div class="flex items-center gap-3 mb-3">
            <div class="w-12 h-12 rounded-lg bg-red-500/10 flex items-center justify-center text-2xl">\U0001f4c9</div>
            <h3 class="text-base font-semibold text-white group-hover:text-red-500 transition">Bear Put Spread</h3>
          </div>
          <p class="text-sm text-gray-500">Bearish debit spread using put options with defined risk and automated order execution.</p>
        </a>
      </div>

      <h2 class="text-2xl font-bold text-white mb-3">Portfolio Strategies</h2>
      <p class="text-gray-400 mb-8">Automated portfolio creation, rebalancing, and performance tracking across multiple asset classes.</p>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <a href="bitcoin-etf-portfolio-flow.html" class="group bg-gray-900/40 border border-white/10 rounded-xl p-6 hover:border-amber-500/40 hover:bg-amber-500/5 transition-all">
          <div class="flex items-center gap-3 mb-3">
            <div class="w-12 h-12 rounded-lg bg-amber-500/10 flex items-center justify-center text-2xl">\u20bf</div>
            <h3 class="text-base font-semibold text-white group-hover:text-amber-500 transition">Bitcoin ETF Portfolio</h3>
          </div>
          <p class="text-sm text-gray-500">Diversified portfolio of 11 Bitcoin ETFs with automated buy, sell, and performance tracking.</p>
        </a>
        <a href="crypto-portfolio-flow.html" class="group bg-gray-900/40 border border-white/10 rounded-xl p-6 hover:border-purple-500/40 hover:bg-purple-500/5 transition-all">
          <div class="flex items-center gap-3 mb-3">
            <div class="w-12 h-12 rounded-lg bg-purple-500/10 flex items-center justify-center text-2xl">\U0001fa99</div>
            <h3 class="text-base font-semibold text-white group-hover:text-purple-500 transition">Crypto Portfolio</h3>
          </div>
          <p class="text-sm text-gray-500">Portfolio of 17 cryptocurrency assets with automated management and analytics.</p>
        </a>
        <a href="faang-portfolio-flow.html" class="group bg-gray-900/40 border border-white/10 rounded-xl p-6 hover:border-blue-500/40 hover:bg-blue-500/5 transition-all">
          <div class="flex items-center gap-3 mb-3">
            <div class="w-12 h-12 rounded-lg bg-blue-500/10 flex items-center justify-center text-2xl">\U0001f4ca</div>
            <h3 class="text-base font-semibold text-white group-hover:text-blue-500 transition">FAANG Portfolio</h3>
          </div>
          <p class="text-sm text-gray-500">Major tech stock portfolio with position management and performance tracking.</p>
        </a>
      </div>

    </div>
  </section>

  <!-- ============ CTA ============ -->
  <section class="border-t border-white/5 py-24 text-center">
    <div class="max-w-3xl mx-auto px-6">
      <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight mb-6 text-white">Ready to Automate Your Trading?</h2>
      <p class="text-gray-400 text-lg mb-10">Import any flow into your MachineTrader\u2122 instance and start trading in minutes.</p>
      <a href="../index.html#pricing" class="btn-primary text-lg font-semibold px-10 py-4 rounded-full inline-flex items-center gap-2">
        Start Free Trial
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
      </a>
    </div>
  </section>

  <!-- ============ FOOTER ============ -->
  <footer class="bg-gray-950 border-t border-white/10">
    <div class="max-w-7xl mx-auto px-6 lg:px-8 py-16">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-10 mb-16">
        <div class="col-span-2 md:col-span-1">
          <a href="../index.html" class="flex items-center gap-2 mb-4">
            <img src="../images/logo.svg" alt="MachineTrader" class="h-8 w-auto" />
            <span class="text-lg font-bold text-white">MachineTrader\u2122</span>
          </a>
          <p class="text-sm text-gray-500 leading-relaxed">Automate your trading strategies using our low-code/no-code MachineTrader\u2122 software.</p>
        </div>
        <div>
          <h4 class="text-sm font-semibold text-brand-500 uppercase mb-4">Product</h4>
          <ul class="space-y-3 text-sm text-gray-500">
            <li><a href="../features.html" class="hover:text-white transition">Features</a></li>
            <li><a href="../index.html#pricing" class="hover:text-white transition">Pricing</a></li>
            <li><a href="../data-center.html" class="hover:text-white transition">Data Center</a></li>
            <li><a href="index.html" class="hover:text-white transition">Trading Scripts</a></li>
            <li><a href="../backtests.html" class="hover:text-white transition">Backtests</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-sm font-semibold text-brand-500 uppercase mb-4">Resources</h4>
          <ul class="space-y-3 text-sm text-gray-500">
            <li><a href="../about-us.html" class="hover:text-white transition">About Us</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-sm font-semibold text-brand-500 uppercase mb-4">Legal</h4>
          <ul class="space-y-3 text-sm text-gray-500">
            <li><a href="../privacy-policy.html" class="hover:text-white transition">Privacy Policy</a></li>
            <li><a href="../terms-of-service.html" class="hover:text-white transition">Terms of Service</a></li>
            <li><a href="../cookie-policy.html" class="hover:text-white transition">Cookie Policy</a></li>
          </ul>
        </div>
      </div>
      <div class="border-t border-white/10 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
        <div class="text-sm text-gray-500">\u00a9 2022\u20132026 MachineTrader\u2122. All Rights Reserved. \u00b7 30 Wall Street, 8th Floor, New York, NY 10005</div>
        <div class="flex items-center gap-6">
          <a href="mailto:info@machinetrader.io" class="text-gray-500 hover:text-white transition text-sm">info@machinetrader.io</a>
        </div>
      </div>
    </div>
    <div class="bg-black border-t border-white/5">
      <div class="max-w-7xl mx-auto px-6 lg:px-8 py-6">
        <p class="text-xs text-gray-600 leading-relaxed">
          <strong class="text-gray-500">Disclaimer:</strong> MachineTrader provides technology for automated trading. All trading involves risk. Past performance is not indicative of future results. MachineTrader is not a registered broker-dealer or investment advisor. Securities trading is offered through Alpaca Securities LLC, member FINRA/SIPC. *Commission-free for U.S. equities.
        </p>
      </div>
    </div>
  </footer>

  </div><!-- end #page-content -->

  <!-- ============ SCRIPTS ============ -->
  <script>
    const EXPECTED_HASH = '8b32a1ee1c55f72d3dd33bdc6cc54b873d7307fe1972855b1cb2d2d11181222f';
    async function sha256(message) {{
      const msgBuffer = new TextEncoder().encode(message);
      const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
      const hashArray = Array.from(new Uint8Array(hashBuffer));
      return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }}
    (async () => {{
      const lockScreen = document.getElementById('lock-screen');
      const pageContent = document.getElementById('page-content');
      const form = document.getElementById('password-form');
      const input = document.getElementById('password-input');
      const error = document.getElementById('password-error');
      if (sessionStorage.getItem('mt-auth') === EXPECTED_HASH) {{
        lockScreen.classList.add('hidden');
        pageContent.classList.remove('hidden');
      }} else {{ input.focus(); }}
      form.addEventListener('submit', async (e) => {{
        e.preventDefault();
        const hash = await sha256(input.value);
        if (hash === EXPECTED_HASH) {{
          sessionStorage.setItem('mt-auth', EXPECTED_HASH);
          lockScreen.style.transition = 'opacity 0.4s ease';
          lockScreen.style.opacity = '0';
          setTimeout(() => {{ lockScreen.classList.add('hidden'); pageContent.classList.remove('hidden'); }}, 400);
        }} else {{
          error.classList.remove('hidden'); input.classList.add('!border-red-500'); input.value = ''; input.focus();
          setTimeout(() => {{ error.classList.add('hidden'); input.classList.remove('!border-red-500'); }}, 3000);
        }}
      }});
    }})();
  </script>
  <script src="../js/main.js"></script>
</body>
</html>'''


def main():
    files = sorted([f for f in os.listdir(FLOWS_DIR) if f.endswith(".html")])
    print(f"Found {len(files)} trading-flows files to convert.\n")

    for filename in files:
        filepath = os.path.join(FLOWS_DIR, filename)

        # Back up original
        bak_path = filepath + ".bak"
        if not os.path.exists(bak_path):
            with open(filepath, "r", encoding="utf-8") as f:
                orig = f.read()
            with open(bak_path, "w", encoding="utf-8") as f:
                f.write(orig)
            print(f"  Backed up: {filename}")

        if filename == "index.html":
            new_html = generate_index_page()
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_html)
            print(f"  Converted: {filename} (index page)")
            continue

        if filename not in FLOW_META:
            print(f"  SKIPPED: {filename} (no metadata defined)")
            continue

        with open(bak_path, "r", encoding="utf-8") as f:
            content = f.read()

        meta = FLOW_META[filename]
        custom_css = extract_custom_css(content)
        main_content = extract_main_content(content)
        new_html = generate_dark_flow_page(filename, meta, custom_css, main_content)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_html)

        print(f"  Converted: {filename} — {meta['h1']}")

    print(f"\nDone! Converted {len(files)} trading-flows files.")


if __name__ == "__main__":
    main()
