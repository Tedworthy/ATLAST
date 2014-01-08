report:
	pdflatex -shell-escape report.tex
	biber report
	pdflatex -shell-escape report.tex
	pdflatex -shell-escape report.tex

clean:
	rm -rf *.aux *.pdf *.log *.bcf *.bbl *.blg *.bbg *.run.xml
