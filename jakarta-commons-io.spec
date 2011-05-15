# Copyright (c) 2000-2007, JPackage Project
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

%define gcj_support 1

# If you don't want to build with maven, and use straight ant instead,
# give rpmbuild option '--without maven'

%define with_maven %{!?_without_maven:1}%{?_without_maven:0}
%define without_maven %{?_without_maven:1}%{!?_without_maven:0}

%define section   free
%define base_name       commons-io

Name:           jakarta-%{base_name}
Version:        1.4
Release:        %mkrel 2.0.3
Epoch:          0
Summary:        Commons IO Package

Group:          Development/Java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:        Apache License
URL:            http://jakarta.apache.org/commons/io/
#cvs -d :pserver:anoncvs@cvs.apache.org:/home/cvspublic login
#cvs -z3 -d :pserver:anoncvs@cvs.apache.org:/home/cvspublic export -r HEAD jakarta-commons/io
Source0:        commons-io-1.4-src.tar.gz
Source1:        %{name}-settings.xml
Source2:        %{name}-jpp-depmap.xml
Source3:        commons-parent-3.pom
Source4:	%{name}-pom.patch
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
Provides:       %{base_name} = %{epoch}:%{version}-%{release}
BuildRequires:  java-javadoc
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit >= 0:1.6
BuildRequires:  junit >= 0:3.8.1
%if %{with_maven}
BuildRequires:  maven2
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven2-plugin-antrun
BuildRequires:  maven2-plugin-assembly
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-idea
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-resources
%endif


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
cp %{SOURCE1} settings.xml
mkdir -p .m2/repository/JPP/maven2/default_poms
cp %{SOURCE3} .m2/repository/JPP/maven2/default_poms/org.apache.commons-commons-parent.pom
patch <%{SOURCE4}


%build
%if %{with_maven}
sed -i -e "s|<url>__JPP_URL_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__JAVADIR_PLACEHOLDER__</url>|<url>file://`pwd`/external_repo</url>|g" settings.xml
sed -i -e "s|<url>__MAVENREPO_DIR_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__MAVENDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/maven2/plugins</url>|g" settings.xml
sed -i -e "s|<url>__ECLIPSEDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/eclipse/plugins</url>|g" settings.xml

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mkdir external_repo
ln -s %{_javadir} external_repo/JPP

mvn-jpp \
        -e \
        -s $(pwd)/settings.xml \
        -Dmaven.test.failure.ignore=true \
        -Dmaven2.jpp.mode=true \
        -Dmaven2.jpp.depmap.file=%{SOURCE2} \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc
%else

export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=
CLASSPATH=target/classes:target/test-classes:$CLASSPATH
%ant -Dbuild.sysclasspath=only dist

%endif


%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
%if %{with_maven}
install -pm 644 target/%{base_name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
%else
install -pm 644 build/%{base_name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
%endif
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
ln -s %{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{base_name}-%{version}.jar
ln -s %{base_name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{base_name}.jar

%add_to_maven_depmap %{base_name} %{base_name} %{version} JPP %{base_name}

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}.pom

install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%if %{with_maven}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%else
unzip -q build/dist/%{base_name}-%{version}.zip %{base_name}-%{version}/docs/* -d $RPM_BUILD_ROOT%{_javadocdir}
mv $RPM_BUILD_ROOT%{_javadocdir}/%{base_name}-%{version}/docs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
rm -r $RPM_BUILD_ROOT%{_javadocdir}/%{base_name}-%{version}
%endif
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} 

%{gcj_compile}

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
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt
%{_javadir}/*.jar
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}
%{gcj_files}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}


