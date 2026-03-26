#!/usr/bin/env python3
"""
ADRENO829 Perfect Fix - Disable GMEM for stability
Based on deep learning analysis of ADRENO829 hardware
"""

import re
import sys

def fix_adreno829():
    file_path = 'src/freedreno/vulkan/tu_device.c'
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
        return False
    
    # Find A8xx initialization section and add ADRENO829 special handling
    adreno829_fix = '''
    // ADRENO829 special handling - disable GMEM for stability
    if (dev_info->chip_id == 0x44030A00) {  // FD829
        tu_env.debug |= TU_DEBUG_DISABLE_GMEM;
        tu_env.debug |= TU_DEBUG_NOLRZ;
        printf("[ADRENO829] GMEM disabled for stability\\n");
    }
'''
    
    # Insert after "case 8:" in A8xx initialization
    pattern = r'(case 8:.*?tu_env\.debug \|= TU_DEBUG_NOLRZ;)'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(
            pattern,
            r'\1' + adreno829_fix,
            content,
            flags=re.DOTALL
        )
        print("✓ Added ADRENO829 special handling to tu_device.c")
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    return True

if __name__ == '__main__':
    success = fix_adreno829()
    sys.exit(0 if success else 1)
