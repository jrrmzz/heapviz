#!/usr/bin/env python3

import json
import pg_logger
import sys

def read_file(name):
    input = open(name)
    try:
        return input.read()
    finally:
        input.close()

def main():
    script_name = sys.argv[1]
    output_name = script_name + '.heapviz.html'
    
    user_script = read_file(script_name)
    template = read_file('heapviz.html')
    
    output = open(output_name, 'wt')
    try:
        starting_instruction = '-1'
        if len(sys.argv) > 2:
            starting_instruction = sys.argv[2]
        
        json_output = ''
        def output_handler(input_code, output_trace):
            nonlocal json_output
            ret = dict(code=input_code, trace=output_trace)
            json_output += json.dumps(ret, indent=None)
        
        cumulative_mode = False
        pg_logger.exec_script_str(user_script, cumulative_mode, output_handler)
    
        template = template.replace('${JSON_TRACE}', json_output)
        template = template.replace('${STARTING_INSTRUCTION}', starting_instruction);
        print(template, file=output)
    finally:
        output.close()

if __name__ == '__main__':
    main()