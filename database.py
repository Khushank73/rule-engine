import mysql.connector
import json
from config import DB_CONFIG
from rule_ast import Node

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def store_rule(rule_string, ast):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Rules (rule_string, ast_json) 
        VALUES (%s, %s);
    """, (rule_string, json.dumps(ast.__dict__)))
    conn.commit()
    rule_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return rule_id

def load_rule(rule_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT rule_string, ast_json FROM Rules WHERE id = %s;
    """, (rule_id,))
    result = cursor.fetchone()
    conn.close()
    
    # Reconstruct the AST from the stored JSON
    ast = json.loads(result['ast_json'])
    ast_node = reconstruct_ast(ast)
    
    return {
        "rule_string": result['rule_string'],
        "ast": ast_node
    }

def reconstruct_ast(data):
    if 'type' in data and data['type'] == 'operator':
        left = reconstruct_ast(data['left'])
        right = reconstruct_ast(data['right'])
        return Node('operator', left, right, data['value'])
    elif 'type' in data and data['type'] == 'operand':
        return Node('operand', value=data['value'])
    else:
        raise ValueError(f"Unexpected AST node format: {data}")
