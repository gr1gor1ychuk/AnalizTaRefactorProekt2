import xml.etree.ElementTree as ET
import os

def fix_coverage_paths():
    tree = ET.parse('coverage.xml')
    root = tree.getroot()
    
    # Fix source paths
    for source in root.findall('.//source'):
        source.text = os.path.abspath('src')
    
    # Fix file paths in classes
    for class_elem in root.findall('.//class'):
        filename = class_elem.get('filename')
        if filename:
            # Convert to absolute path
            abs_path = os.path.join('src', filename)
            class_elem.set('filename', abs_path)
    
    # Save the modified XML
    tree.write('coverage.xml', encoding='UTF-8', xml_declaration=True)

if __name__ == '__main__':
    fix_coverage_paths() 