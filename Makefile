
TARGET= GameOfLife
VERSION= 0.0.13
QVERSION= "'${VERSION}'"
VERSION_FILE= VERSION

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

UPDTINIT = 's/__version__.*=.*/__version__ = ${QVERSION}/'
UPDTRDME = 's/Version: .*/Version: ${VERSION}/'

all:
	@echo "make update  - updates the version"
	@echo "make sdist   - creates a source distribution"
	@echo "make bdist   - creates a binary distribution"
	@echo "make test    - runs unit tests"
	@echo "make upload  - uploads bdist_wheel to PYPI=${PYPI}"
	@echo "make clean   - removes all derived files and directories"

update:
	@echo ${VERSION} > ${VERSION_FILE}
	@${SED} -e ${UPDTINIT} ${PKG_INIT} > ${PKG_INIT}.tmp
	@${MV} ${PKG_INIT}.tmp ${PKG_INIT}
	@${SED} -e ${UPDTRDME} ${README} > ${README}.tmp
	@${MV} ${README}.tmp ${README}

sdist:
	${PYSETUP} build sdist

wheel:
	${PYSETUP} build bdist_wheel

bdist:
	${PYSETUP} build bdist

test:
	${PYSETUP} test

# switch to twine?

upload:
	$(PYSETUP) bdist_wheel upload -r ${PYPI}


clean:
	@${PYSETUP} clean
	@${RM} -rf ${TMPFILES}
