# DataList

## Frontend
### DOM

```
.<name>-container*
      \__.<name>-entry-wrapper[data-id=<id froms server>]
               \__ .<name>-button-edit*
               \__ .<name>-button-remove*
               \__ <other contents>*
      \__ <multiple .<name>-entry-wrapper, each with corresponding ids>

*: must be defined by user
```
### JavaScript
	DataList(name: str, container: jQuery, render_data: function) -> DataList
    	name: <name> above
        container: .<name>-container
        render_data: a function(data) which renders HTML string from data passed.

	DataList.load()
    	- $.getJSON to /ajax/<name>/get to get available data
    	- for each entry, call DataList.render()

    DataList.render(data)
    	- call DataList.render_data to get HTML string
    	- Wrap it around .<name>-entry-wrapper[data-id=data.id]
    	- Append it into DataList.container
    	- Bind (.<name>-entry-wrapper[data-id=data.id] => button-edit) to DataList.edit()
    	- Bind (.<name>-entry-wrapper[data-id=data.id] => button-remove) to DataList.remove()

    DataList.add(data)
    	- $.post to /ajax/<name>/add to get id
    	- Call DataList.render(data)

    DataList.remove(id)
    	-$.post to /ajax/<name>/remove to remove id
        - get wrapper of id
        - wrapper.remove()

	DataList.edit(id):
    	TBD

## Backend

### AJAX
* ```/ajax/<name>/get```: get all records
* ```/ajax/<name>/add```: add record
* ```/ajax/<name>/remove```: remove record

### Python
	- DataList.__init__(name: str) -> DataList
	- @DataList.get: decorator to function get() => list of entries
	- @DataList.add: decorator to function add(value) => id: string
	- @DataList.remove: decorator to function remove(id) => boolean
	- DataList.get_url_endpoint()


## Frontend <=> Backend JSON
### ``entry`` object
```
<nothing, just a GET request>
```
```
{
	"id": <id of entry, usually id in database>,
    "value": <value of entry, can be anything>
}
```
### ``/ajax/<name>/get``
```
{
	entries: [
    	multiple "entry" objects
    ]
}
```
### ``/ajax/<name>/add``
```
{
	"data": <data>
}
```
```
{
	"id": <id of newly added data>
}
```
### ``/ajax/<name>/remove``
```
{
	"id": <id of entry>
}
```
```
{
	"status": "ok" | ...
}
```