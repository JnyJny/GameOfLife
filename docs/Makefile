TARGET= GameOfLife

CELL= ${TARGET}.cell
WOLRD= ${TARGET}.world
PATTERNS= ${TARGET}.patterns

TESTS= ${TARGET}.tests
TEST_CELL= ${TESTS}.test_cell
TEST_WORLD= ${TESTS}.test_world
TEST_PATTERNS= ${TESTS}.test_patterns

THINGS = ${TARGET} ${CELL} ${WORLD} ${PATTERNS} \
	${TESTS} ${TEST_CELL} ${TEST_WORLD} ${TEST_PATTERNS}

HTML = ${THINGS:=.html}

GIT= git
RM= rm -f
PYDOC= pydoc3
PYDOCFLAGS= -w

BRANCH= gh-pages


all:
	@echo "make html    - generates HTML files using PYDOC=${PYDOC}"
	@echo "make publish - generates HTML files and pushes BRANCH=${BRANCH}"


publish: html
	git add ${HTML}

html: ${HTML}

${TARGET}.html: 
	${PYDOC} ${PYDOCFLAGS} ${TARGET}

${CELL}.html:
	${PYDOC} ${PYDOCFLAGS} ${CELL}

${WORLD}.html:
	${PYDOC} ${PYDOCFLAGS} ${WORLD}

${PATTERNS}.html:
	${PYDOC} ${PYDOCFLAGS} ${PATTERNS}

${TESTS}.html:
	${PYDOC} ${PYDOCFLAGS} ${TESTS}

${TEST_CELL}.html:
	${PYDOC} ${PYDOCFLAGS} ${TEST_CELL}

${TEST_WORLD}.html:
	${PYDOC} ${PYDOCFLAGS} ${TEST_WORLD}

${TEST_PATTERNS}.html:
	${PYDOC} ${PYDOCFLAGS} ${TEST_PATTERNS}

clean:
	@${RM} ${HTML} *~
