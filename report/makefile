
.PHONY: clean

all: report


max: clean report
	scp report.pdf mt3410@shell1.doc.ic.ac.uk:/homes/mt3410/public_html/report.pdf


report:
	pdflatex -shell-escape report.tex
	biber report
	pdflatex -shell-escape report.tex
	pdflatex -shell-escape report.tex

clean:
	-rm -rf *.aux 
	-rm -rf *.pdf 
	-rm -rf *.log 
	-rm -rf *.bcf 
	-rm -rf *.bbl 
	-rm -rf *.blg 
	-rm -rf *.bbg 
	-rm -rf *.run.xml 
	-rm -rf *.toc
	-rm -rf *.out
