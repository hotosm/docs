# Licensing

With so many options for licensing code, the topic can be quite
confusing. Many projects like Boost, Eclipse, Apache, etc.. have their
own license, often based on the
[GPL](https://en.wikipedia.org/wiki/GNU_General_Public_License), which
only apply to that project, so aren't appropriate for use at
HOT. There are two primary types of licenses, permissive and
non-permissive. Non permissive licenses may appear to be open source,
but often it's a few clauses in the licenses that make them unable to
be used in other open source projects.

HOT believes strongly in the freedoms embodied on the [free
software](https://en.wikipedia.org/wiki/Free_software) culture, while
following the collaborative development processes common for open
source software projects.

All of the software at HOT uses permissive licenses, commonly the
GPLv3 for compiled code, the AGPLv3 for code shared over a network (a
website), and some older code using the BSD license or pubic domain.

## The GPLv3 and AGPLv3

- These are strong 'copyleft' licences, meaning that anyone
  modifiying the software is required to make those changes openly
  available. This is commonly called the derivative work clause. Any
  derivative software must be contributes it back to the original
  software project with no restrictions.

- The main purpose of this license is to prevent commercial
  exploitation of open code, making any modifications open so the
  entire community can benefit.

- The distinction between the two is that AGPL is used for code
  distributed via a network (i.e. a website), whereas, GPL can be
  used for all other code (e.g. PyPi packages).

> Originally HOT was using BSD-2-Clause, which is more permissive
> and not copyleft, meaning it is fully open but there is no protection
> from commercial exploitation.
>
> Tools using BSD-2-Clause:
>
> - Tasking Manager
> - Export Tool
> - Open Aerial Map

## Other Content is CC-BY

- Creative content, such as translations and designs are copyrighted
  different.
- As with AGPL for code, this license is 'copyleft'
- It allows others modify and built upon our own, even for commercial
  purposes, as long as they **credit us** and
  **license their work under the same terms as CC-BY**.
- The current CC-BY license available would be
  Creative Commons Attribution 4.0 International.

## What Licenses Can We Use

- We use many underlying packages and tools within our software.
- Any contributor must be aware of licensing before adding any
  additional external code to our software.

### Compatible Licenses

This is a short list of copyleft compatible licenses. For more detail,
refer to the Free Software Foundation (FSF) page on [compatible and
incompatible
licenses](https://www.gnu.org/licenses/license-list.en.html). This in
far from an exhaustive list, only the most common ones are listed
here.

- Public Domain
- Mozilla Public License (MPL) version 2.0
- Apache License 2.0
- Modified BSD license
- Intel Open Source License
- FreeBSD license

### Uncertain Licenses

Being technologists, and not lawyers, we do not have the time or
expertise to identify and assess every license type available.

There are some licenses that could potentially be compatible,
but we do not have a well formed opinion about their usage.
Typically we would defer to an authority such as the FSF.

These licenses may include, but are not limited to:

- EUPL-1.2

For the moment we do not expressly forbid their usage, but the
rationale for doing so should be explained on a case-by-case basis.

### Incompatible Licenses

The Open Source Initiative also has a list of [approved open source
licenses](https://opensource.org/licenses). Not all of these are
compatible with copylefted software, so may not be appropriate for code at
HOT even though they are considered permissive licenses.

Licenses that can't be used for any code in HOT software projects:

- Mozilla Public License (MPL) version 1.1
- Apache License, Version 1.0 and 1.1
- Apple Public Source License (APSL), version 2
- Microsoft Public License (Ms-PL)
- NASA Open Source Agreement
- Original BSD license
- Common Development and Distribution License (CDDL), version 1.0
- Common Public Attribution License 1.0 (CPAL)
- Common Public License Version 1.0
- European Union Public License (EUPL) version 1.1 and 1.2
- IBM Public License, Version 1.0
- Open Software License, all versions through 3.0
