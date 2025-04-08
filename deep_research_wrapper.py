import os
import subprocess
import json
import tempfile

def execute_deep_research(query, breadth=3, depth=2):
    # Create a temporary JavaScript file to run deep-research.
    js_script = f"""
    const {{ deepResearch }} = require('deep-research');
    
    async function runResearch() {{
        try {{
            const result = await deepResearch({{
                query: "{query.replace('"', '\\"')}",
                breadth: {breadth},
                depth: {depth}
            }});
            console.log(JSON.stringify(result));
        }} catch (error) {{
            console.error(error.message);
            process.exit(1);
        }}
    }}
    runResearch();
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write(js_script)
        script_path = f.name

    try:
        env = os.environ.copy()
        if "FIRECRAWL_KEY" not in env or "OPENAI_KEY" not in env:
            raise ValueError("Missing FIRECRAWL_KEY or OPENAI_KEY")
        result = subprocess.run(
            ["node", script_path],
            capture_output=True,
            text=True,
            env=env
        )
        if result.returncode != 0:
            raise Exception(f"Deep research failed: {result.stderr}")
        return json.loads(result.stdout)
    finally:
        os.unlink(script_path)
