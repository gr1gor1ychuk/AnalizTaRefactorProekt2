import xml.etree.ElementTree as ET
import os

def fix_coverage_paths():
    tree = ET.parse('coverage.xml')
    root = tree.getroot()
    
    # Fix source paths
    for source in root.findall('.//source'):
        path = source.text
        if path:
            # Convert Windows path to Unix-style
            path = path.replace('\\', '/')
            # Remove drive letter and make path relative
            if ':' in path:
                path = path.split(':', 1)[1]
            # Remove leading slashes
            path = path.lstrip('/')
            # Make path relative to project root
            if 'src' in path:
                path = 'src'
            source.text = path
    
    # Fix file paths in classes
    for class_elem in root.findall('.//class'):
        filename = class_elem.get('filename')
        if filename:
            # Convert Windows path to Unix-style
            filename = filename.replace('\\', '/')
            # Make path relative to src directory
            if '/' in filename:
                filename = filename.split('/')[-1]
            class_elem.set('filename', filename)
    
    tree.write('coverage.xml', encoding='UTF-8', xml_declaration=True)

if __name__ == '__main__':
    fix_coverage_paths() 