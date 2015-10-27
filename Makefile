TARGET= GameOfLife

MAJOR=0
MINOR=0
POINT=17
VERSION= ${MAJOR}.${MINOR}.${POINT}
QVERSION= "'${VERSION}'"
VERSION_FILE= VERSION
NEWPOINT = `expr $(POINT) + 1`
NEWMINOR = `expr $(MINOR) + 1`
NEWMAJOR = `expr $(MAJOR) + 1`
UPDTINIT = 's/__version__.*=.*/__version__ = ${QVERSION}/'
UPDTRDME = 's/Version: .*/Version: ${VERSION}/'

MAKEFILE= Makefile

PYTHON=python3
SETUP= setup.py
PYSETUP= ${PYTHON} ${SETUP}

PYPI= pypitest

PKG_ROOT= ${TARGET}
PKG_INIT = ${PKG_ROOT}/__init__.py
README = README.md

TMPFILES= VERSION dist build ${TARGET}.egg-info

SED = sed
RM = rm
MV = mv

all:
	@echo "make sdist      - creates a source distribution"
	@echo "make bdist      - creates a binary distribution"
	@echo "make wheel      - creates a wheel distribution"
	@echo "make test       - runs unit tests"
	@echo "make upload     - uploads bdist_wheel to PYPI=${PYPI}"
	@echo "make clean      - removes all derived files and directories"
	@echo "make bump_major - increment the major version number MAJOR=${MAJOR}"
	@echo "make bump_minor - increment the minor version number MINOR=${MINOR}"
	@echo "make bump_point - increment the point version number POINT=${POINT}"
	@echo "make update     - updates the version VERSION=${VERSION}"


bump_major:
	@${SED} "s/^MAJOR[ \t]*=[ \t]*[0-9]*/MAJOR=$(NEWMAJOR)/" \
	  ${MAKEFILE} > ${MAKEFILE}.tmp
	@${MV} ${MAKEFILE}.tmp ${MAKEFILE}

bump_minor:
	@${SED} "s/^MINOR[ \t]*=[ \t]*[0-9]*/MINOR=$(NEWMINOR)/" \
	  ${MAKEFILE} > ${MAKEFILE}.tmp
	@${MV} ${MAKEFILE}.tmp ${MAKEFILE}

bump_point:
	@${SED} "s/^POINT[ \t]*=[ \t]*[0-9]*/POINT=$(NEWPOINT)/" \
	  ${MAKEFILE} > ${MAKEFILE}.tmp
		@${MV} ${MAKEFILE}.tmp ${MAKEFILE}

update:
	@echo ${VERSION} > ${VERSION_FILE}
	@${SED} -e ${UPDTINIT} ${PKG_INIT} > ${PKG_INIT}.tmp
	@${MV} ${PKG_INIT}.tmp ${PKG_INIT}
	@${SED} -e ${UPDTRDME} ${README} > ${README}.tmp
	@${MV} ${README}.tmp ${README}


tag:
	git tag ${VERSION}
	git push origin ${VERSION}

sdist:
	${PYSETUP} build sdist

wheel:
	${PYSETUP} build bdist_wheel

bdist:
	${PYSETUP} build bdist

test:
	${PYSETUP} test -q

# switch to twine?

upload:
	$(PYSETUP) bdist_wheel upload -r ${PYPI}

clean:
	@${PYSETUP} clean
	@${RM} -rf ${TMPFILES}
