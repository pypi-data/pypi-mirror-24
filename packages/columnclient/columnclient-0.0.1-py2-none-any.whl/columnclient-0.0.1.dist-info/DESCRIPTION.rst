Column is a thin wrapper on top of ansible API, to serve
as an entry point for other code when ansible is needed. As ansible
internal API is not officially exposed and thus changes are very likely,
this wrapper should be used instead of touching ansible directly,
so that any further ansible API change will only incur change in this module.



