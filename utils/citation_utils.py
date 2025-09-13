import json
import logging
from datetime import datetime
import bibtexparser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def strip_braces(text):
    """
    Removes curly braces from a string.
    """
    if text:
        return text.replace("{", "").replace("}", "")
    return text

def format_citation_apa(citation):
    """
    Formats a citation dictionary into APA style with clickable links.
    Replaces {CURRENT_YEAR} with the current year.
    """
    try:
        current_year = datetime.now().year
        author = strip_braces(citation.get('author', 'Unknown Author'))
        year = strip_braces(citation.get('year', 'n.d.')).replace("CURRENT_YEAR", str(current_year))
        title = strip_braces(citation.get('title', 'Untitled'))
        url = strip_braces(citation.get('url', ''))
        publisher = strip_braces(citation.get('publisher', ''))

        if url:
            if publisher:
                formatted_citation = (
                    f"{author} ({year}). <i>{title}</i>. {publisher}. Retrieved from "
                    f'<a href="{url}" target="_blank">{url}</a>'
                )
            else:
                formatted_citation = (
                    f"{author} ({year}). <i>{title}</i>. Retrieved from "
                    f'<a href="{url}" target="_blank">{url}</a>'
                )
        else:
            if publisher:
                formatted_citation = f"{author} ({year}). <i>{title}</i>. {publisher}."
            else:
                formatted_citation = f"{author} ({year}). <i>{title}</i>."

        return formatted_citation
    except Exception as e:
        print(f"Error formatting citation: {e}")
        return "Invalid citation format."

def load_bib_file(filepath):
    """
    Loads and parses a .bib file into a dictionary.
    """
    try:
        with open(filepath, encoding='utf-8') as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
        citations = {entry['ID']: entry for entry in bib_database.entries}
        logging.info("Loaded citations from .bib file.")
        for cite_id, entry in citations.items():
            logging.debug(f"- {cite_id}: {entry.get('title', 'No title')}")
        return citations
    except Exception as e:
        logging.error(f"Error loading .bib file: {e}")
        return {}

def load_json_file(filepath):
    """
    Loads a JSON file.
    """
    try:
        with open(filepath) as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"JSON file not found at {filepath}.")
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {filepath}: {e}")
        return {}

def get_citation(cite_id, citations):
    """
    Retrieves a citation entry from the citations dictionary and formats it in APA style.
    """
    cite_id = cite_id.strip()
    logging.debug(f"Looking up citation for ID: {cite_id}")
    if cite_id in citations:
        citation = citations[cite_id]
        logging.debug(f"Found citation for ID: {cite_id}")
        return format_citation_apa(citation)
    else:
        logging.warning(f"Citation ID '{cite_id}' not found in .bib file.")
        return None

def validate_and_get_references(items, citations, project_data, key='cite', project_key='project'):
    """
    Validates items in JSON and retrieves corresponding APA-formatted citations.
    """
    unique_citations = set()
    formatted_citations = []

    for item in items:
        if isinstance(item, dict):
            cite_id = item.get(key)

            if not cite_id and project_key in item:
                project_name = item[project_key]
                matching_project = next(
                    (proj for proj in project_data.values() if proj.get("name") == project_name),
                    None
                )
                if matching_project:
                    cite_id = matching_project.get(key)

            if cite_id and cite_id not in unique_citations:
                unique_citations.add(cite_id)
                citation = get_citation(cite_id, citations)
                if citation:
                    formatted_citations.append(citation)
                else:
                    logging.warning(f"Citation ID '{cite_id}' not found in .bib file.")

    return formatted_citations

def load_references():
    """
    Loads and processes references from JSON configuration files and .bib file.
    Formats citations in APA style and ensures uniqueness.
    """
    citations = load_bib_file('static/config/references.bib')
    layers = load_json_file('static/config/layers.json')
    mobile_stations = load_json_file('static/config/mobile_stations.json')
    fixed_stations = load_json_file('static/config/fixed_stations.json')
    project_data = load_json_file('static/config/project.json')

    all_layers = layers.get("baseMaps", []) + layers.get("additionalLayers", [])
    references = {
        "map_sources": validate_and_get_references(all_layers, citations, project_data),
        "mobile_station_sources": validate_and_get_references(mobile_stations, citations, project_data),
        "fixed_station_sources": validate_and_get_references(fixed_stations, citations, project_data)
    }

    return references

def test_bib_file(filepath):
    try:
        with open(filepath) as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
        logging.info("Loaded citations:")
        for entry in bib_database.entries:
            logging.debug(f"- {entry['ID']}: {entry.get('title', 'No title')}")
    except Exception as e:
        logging.error(f"Error parsing .bib file: {e}")

if __name__ == "__main__":
    test_bib_file('static/config/references.bib')
