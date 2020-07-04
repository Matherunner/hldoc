\ProvidesClass{hlprtikz}[2018/07/22 version 1.0 HLPR Tikz Template]
\NeedsTeXFormat{LaTeX2e}

\newif\ifhlpr@smallerfont
\DeclareOption{smaller}{\hlpr@smallerfonttrue}
\ProcessOptions\relax

\LoadClass[tikz]{standalone}

\RequirePackage{amsmath}
\RequirePackage{fontspec}
\RequirePackage{unicode-math}

\setmainfont{Baskerville 10 Pro}[Numbers=Proportional]
\setmonofont{Input Mono}

\ifhlpr@smallerfont
  \setmathfont[
    SizeFeatures={
      {Size=-8.2, Script=Math, Style=MathScriptScript},
      {Size=8.2-12.2, Script=Math, Style=MathScript},
      {Size=12.2-, Script=Math},
    },
  ]{Dark Modern Math Regular}
\else
  \setmathfont[
    SizeFeatures={
      {Size=-10.2, Script=Math, Style=MathScriptScript},
      {Size=10.2-14.5, Script=Math, Style=MathScript},
      {Size=14.5-, Script=Math},
    },
  ]{Dark Modern Math Regular}
\fi

\usetikzlibrary{
  angles,
  arrows.meta,
  calc,
  chains,
  intersections,
  positioning,
  quotes,
  scopes,
  shapes,
  through,
}

\newlength{\hlpr@baselw}
\setlength{\hlpr@baselw}{1bp}

\providecommand{\FSNegTwo}{\fontsize{11bp}{13bp}\selectfont}
\providecommand{\FSNegOne}{\fontsize{14bp}{16bp}\selectfont}
\providecommand{\FSZero}{\fontsize{17bp}{20bp}\selectfont}
\providecommand{\FSOne}{\fontsize{20bp}{23bp}\selectfont}
\providecommand{\FSTwo}{\fontsize{23bp}{26bp}\selectfont}
\providecommand{\FSThree}{\fontsize{25bp}{28bp}\selectfont}

\colorlet{darkRed50}{red!50!black}
\colorlet{red20}{red!20!white}
\colorlet{darkBlue50}{blue!50!black}
\colorlet{green50}{green!50!white}
\colorlet{green20}{green!20!white}
\colorlet{brown80}{brown!80!white}
\colorlet{brown20}{brown!20!white}
\colorlet{gray50}{black!50}
\colorlet{gray20}{black!20}
\colorlet{gray5}{black!5}

% Line widths
\tikzset{
  ultra thin/.style = {line width=0.25\hlpr@baselw},
  very thin/.style = {line width=0.5\hlpr@baselw},
  thin/.style = {line width=1\hlpr@baselw},
  semithick/.style = {line width=1.5\hlpr@baselw},
  thick/.style = {line width=2\hlpr@baselw},
  very thick/.style = {line width=3\hlpr@baselw},
  ultra thick/.style = {line width=4\hlpr@baselw},
}

% Font sizes
\tikzset{
  fsn2/.style = {font=\FSNegTwo},
  fsn1/.style = {font=\FSNegOne},
  fs0/.style = {font=\FSZero},
  fs1/.style = {font=\FSOne},
  fs2/.style = {font=\FSTwo},
  fs3/.style = {font=\FSThree},
}

% Flowcharts
\tikzset{
  fcbase/.style = {on chain, align=center},
  yesno/.style = {font=\FSZero\scshape},
  every join/.style = {->},
}

% General
\tikzset{
  every picture/.style = {
    thin,
    x=1bp,
    y=1bp,
    z=-0.385bp,
    >=latex,
  },
}

\ifhlpr@smallerfont
  \tikzset{
    every picture/.append style = {fsn1},
  }
\else
  \tikzset{
    every picture/.append style = {fs0},
  }
  \fi

\pgfmathsetmacro{\DotRadius}{2}
