"""HTML Parser for Codeforces problem statements and editorials."""

import gzip
import re
import urllib.request
import urllib.error
import bs4
from typing import Dict, Any, List, Optional

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}


def clean_element_text(element: bs4.Tag) -> str:
    """Clean text from a BeautifulSoup element, normalizing whitespace."""
    if not element:
        return ""
    text = element.get_text(separator=' ', strip=True)
    # Normalize multiple spaces
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()


def parse_statement_html(html_bytes: bytes, problem_url: str) -> Dict[str, Any]:
    """Parse raw bytes of a problem page into structured statement data."""
    # Check for PDF
    if html_bytes.startswith(b'%PDF'):
        return {
            'statement_status': 'pdf_attachment',
            'description': f"[Problem statement is a PDF document available at: {problem_url}]",
            'input_specification': "Refer to PDF problem statement",
            'output_specification': "Refer to PDF problem statement",
            'sample_testcases': [],
            'time_limit': None,
            'memory_limit': None,
            'editorial_url': None
        }

    # Decompress gzip if needed
    if html_bytes[:2] == b'\x1f\x8b':
        try:
            html_bytes = gzip.decompress(html_bytes)
        except Exception:
            pass

    html_str = html_bytes.decode('utf-8', errors='replace')
    soup = bs4.BeautifulSoup(html_str, 'html.parser')

    statement = soup.find('div', class_='problem-statement')
    if not statement:
        return {
            'statement_status': 'no_statement',
            'description': None,
            'input_specification': None,
            'output_specification': None,
            'sample_testcases': [],
            'time_limit': None,
            'memory_limit': None,
            'editorial_url': None
        }

    # Limits
    time_lim = statement.find('div', class_='time-limit')
    mem_lim = statement.find('div', class_='memory-limit')
    time_str = clean_element_text(time_lim).replace('time limit per test', '').strip() if time_lim else ''
    mem_str = clean_element_text(mem_lim).replace('memory limit per test', '').strip() if mem_lim else ''

    # Editorial URL from sidebar
    editorial_url = None
    sidebar = soup.find('div', id='sidebar')
    if sidebar:
        for a in sidebar.find_all('a'):
            txt = a.text.lower()
            if any(w in txt for w in ['tutorial', 'editorial', 'solution', 'announcement']):
                href = a.get('href', '')
                if href:
                    editorial_url = ('https://codeforces.com' + href) if href.startswith('/') else href
                    # Prefer direct tutorial / editorial over general announcement
                    if 'tutorial' in txt or 'editorial' in txt:
                        break

    # Description
    header = statement.find('div', class_='header')
    desc_parts: List[str] = []
    for elem in statement.children:
        if elem == header or not getattr(elem, 'name', None):
            continue
        classes = getattr(elem, 'get', lambda x, default: [])('class', [])
        # Stop description when encountering subsections
        if any(c in classes for c in ['input-specification', 'output-specification', 'sample-tests', 'sample-test', 'note']):
            break
        text = clean_element_text(elem)
        if text:
            desc_parts.append(text)

    description = '\n\n'.join(desc_parts)

    # Input Specification
    inp_div = statement.find('div', class_='input-specification')
    inp_spec = ""
    if inp_div:
        h = inp_div.find('div', class_='section-title')
        if h:
            h.extract()
        inp_spec = clean_element_text(inp_div)

    # Output Specification
    out_div = statement.find('div', class_='output-specification')
    out_spec = ""
    if out_div:
        h = out_div.find('div', class_='section-title')
        if h:
            h.extract()
        out_spec = clean_element_text(out_div)

    # Sample Testcases
    samples: List[Dict[str, str]] = []
    sample_div = statement.find('div', class_='sample-test')
    if sample_div:
        inputs = sample_div.find_all('div', class_='input')
        outputs = sample_div.find_all('div', class_='output')
        for i_elem, o_elem in zip(inputs, outputs):
            pre_i = i_elem.find('pre')
            pre_o = o_elem.find('pre')
            i_text = pre_i.get_text('\n', strip=True) if pre_i else ''
            o_text = pre_o.get_text('\n', strip=True) if pre_o else ''
            samples.append({'input': i_text, 'output': o_text})

    return {
        'statement_status': 'completed',
        'description': description,
        'input_specification': inp_spec,
        'output_specification': out_spec,
        'sample_testcases': samples,
        'time_limit': time_str,
        'memory_limit': mem_str,
        'editorial_url': editorial_url
    }


def fetch_problem_statement(url: str, timeout: int = 15) -> Dict[str, Any]:
    """Fetch HTML bytes and parse problem statement."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content_enc = resp.headers.get('Content-Encoding', '')
            raw_bytes = resp.read()
            if content_enc == 'gzip' and raw_bytes[:2] != b'\x1f\x8b':
                raw_bytes = gzip.decompress(raw_bytes)
            return parse_statement_html(raw_bytes, url)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {'statement_status': 'not_found', 'error': f'HTTP {e.code}'}
        return {'statement_status': 'error', 'error': f'HTTP {e.code}'}
    except Exception as e:
        return {'statement_status': 'error', 'error': str(e)}
