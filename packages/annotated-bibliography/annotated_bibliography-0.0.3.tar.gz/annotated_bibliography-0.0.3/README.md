# Annotated Bibliography

This is a script to generate annotated bibliography. It is useful for two things:

1. Making a searchable list of papers to put on your website.

2. As a way to annotate papers externally with comments and tags.

## Structure

There are two files you need to fill to use this script. The first should be a simple bibtex file:

    @inproceedings{morstatter2013sample,
      title={Is the Sample Good Enough? Comparing Data from Twitter's Streaming API with Twitter's Firehose.},
      author={Morstatter, Fred and Pfeffer, J{\"u}rgen and Liu, Huan and Carley, Kathleen M},
      booktitle={ICWSM},
      year={2013}
     }
    
    @inproceedings{tsur2012s,
      title={What's in a hashtag?: content based prediction of the spread of ideas in microblogging communities},
      author={Tsur, Oren and Rappoport, Ari},
      booktitle={Proceedings of the fifth ACM international conference on Web search and data mining},
      pages={643--652},
      year={2012},
      organization={ACM}
    }


The second is a bit more specific, for each entry in the bibtex file, you should create entry in a markdown file:

    ### morstatter2013sample  
    
    ## tag1, tag2
    
    # Title 1
    
    this is an [hyperlink](www.google.com.br)
    
    ### tsur2012s
    
    ## tag3, tag2
    
    # Title 2
    
    this is also an annotation with some formula $\sum_{i=0}^{10} x_i
    
Notice that the structure is as follows: 

- a subsubsection header \### with the bibtex shortcut, 
- a subsection header \## with the tags separated by a comma, 
- a section header \# with the title (optional).
- some comment. It may include links formulas and images, do it the markdown way.

## Installing and running it

    pip3 install annotated_bibliography

    make_ann_bib bibtex.bib mardown.md output.html
        
You should get something like this:

![](annotated_bibliography/example/example.png)

## Dependencies

    matplotlib numpy pybtex mistune jinja2
