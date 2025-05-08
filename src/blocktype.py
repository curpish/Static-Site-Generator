from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code' 
    QUOTE = 'quote'   
    UNORDERED_LIST = 'unordered_list' 
    ORDERED_LIST = 'ordered_list'

def block_to_block_type(block):

    #split all lines
    lines = block.splitlines()

    #check if paragraph 
    if lines == [''] or not lines:
        return BlockType.PARAGRAPH

    #check if code 
    if len(lines) >= 2 and lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE

    #check if quote block
    if lines != [] and (all(line.startswith(">") for line in lines)):
        return BlockType.QUOTE    
    
    #check if heading 
    if len(lines) == 1:
        line = lines[0]
        count = 0
        for char in line:
            if char == "#":
                count += 1
            else:
                break
        if count > 0 and count < 7 and len(line) > count and line[count] == " " and line[count+1:].strip():
            return BlockType.HEADING
        
    #check if unordered list     
    if lines and all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    #check if ordered list         
    if lines:
        is_ordered = True
        for idx, line in enumerate(lines, start=1):
            if not line.startswith(f"{idx}. "):
                is_ordered = False
                break
        if is_ordered:
            return BlockType.ORDERED_LIST

    #otherwise it's a paragraph            
    return BlockType.PARAGRAPH






    
    
    