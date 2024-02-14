# conan-xml-security-c

## Build
```bash
$ conan create . --build=missing -s build_type=Release --version 2.0.4
```

### Iterative Build
The above build does multiple steps and exports the package to Conan local cache. We can also build iteratively which would be helpful if we want to troubleshoot any of the intermediate step.

```bash
$ conan source . --version 2.0.4
$ conan install .
$ conan build
$ conan export-pkg . --version 2.0.4 # exports to local cache
```
