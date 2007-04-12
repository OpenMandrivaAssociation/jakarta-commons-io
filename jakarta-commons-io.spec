# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define section         devel
%define base_name       commons-io
%define gcj_support     1

Name:           jakarta-%{base_name}
Version:        1.3.1
Release:        %mkrel 1.1
Epoch:          0
Summary:        Commons IO Package

Group:          Development/Java
License:        Apache License
URL:            http://jakarta.apache.org/commons/io/
#cvs -d :pserver:anoncvs@cvs.apache.org:/home/cvspublic login
#cvs -z3 -d :pserver:anoncvs@cvs.apache.org:/home/cvspublic export -r HEAD jakarta-commons/io
Source0:        http://apache.org/dist/jakarta/commons/io/source/commons-io-%{version}-src.tar.gz
Source1:        http://apache.org/dist/jakarta/commons/io/source/commons-io-%{version}-src.tar.gz.asc
Source2:        http://apache.org/dist/jakarta/commons/io/source/commons-io-%{version}-src.tar.gz.md5
Patch0:         jakarta-commons-io-1.3.1-link-offline.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
#Distribution:   JPackage
#Vendor:         JPackage Project
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
Provides:       %{base_name} = %{epoch}:%{version}-%{release}
BuildRequires:  java-javadoc
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit >= 0:1.6
BuildRequires:  junit >= 0:3.8.1

%description
Commons-IO contains utility classes, stream implementations, 
file filters, and endian classes.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
Javadoc for %{name}


%prep
%setup -q -n %{base_name}-%{version}-src
%patch0 -p1
%{_bindir}/find . -name '*.jar' | %{_bindir}/xargs -t %{__rm}

%build
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=
CLASSPATH=target/classes:target/test-classes:$CLASSPATH
%{ant} dist-jar javadoc

%install
rm -rf $RPM_BUILD_ROOT
install -Dpm 644 build/%{base_name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
ln -s %{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{base_name}-%{version}.jar
ln -s %{base_name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{base_name}.jar
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/dist-build/commons-io-%{version}/docs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}


