# Simple documentation example

This is a simple DocFX site with a couple of inter-linked conceptual topics.
It uses a simple template to generate raw HTML for each conceptual topic, without any of the outer page markup that the regular templates would generate.
The import script scans the generated `xrefmap.yml`, and then retrieves each topic and inserts it into Confluence.

To build it and host it, run:

```
docfx --port 9090 --serve
```
