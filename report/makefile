
.PHONY: clean

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
