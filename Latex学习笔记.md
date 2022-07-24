[toc]



# Latex

latex中的命令以`\`开头，`{}`表示必选参数，`[]`表示可选参数，`%`表示注释

## 结构

```latex
% preamble 前言部分 导包环境配置
\documentclass[]{} 
\begin{document}
% 正文 类似main 
\maketitle % 显示前言中的信息
\end{document}
```



section

```latex
\sectione{} 新的章节
\subsection{} 二级章节
\subsubsection{} 三级章节
```



text

```latex
\textbf{} 加粗
\textit{} 斜体
\underline{} 下划线
% 两个回车才会换行 
```

## 表格

```latex
\begin{table}
\begin{tabular}
\end{tabular}
\end{table}
```



## 图片

前言中需要导包`\usepackage{graphicx}`

```latex
\begin{figure}
\centering
\includegraphics[width=0.5\textwidth]{test} % 缩放为0.5
\caption{test}\label{test}
\end{figure}
```

## 公式

```latex
\begin{equation}
\end{equation}
```



## 列表

```latex
% 无序列表
\begin{itemize}
\item item1
\end{itemize}

% 有序列表
\begin{enumerate}
\item item1 
\end{enumerate}
```



## 浮动位置

htbp ，这些参数会让latex考虑如此排版，但并不能强制。因为latex的排版系统会考虑页面的利用程度。

![image-20220324222009718](../../../我的坚果云/学习笔记/md_assets/image-20220324222009718.png)



## 引用

`ref{label}` ，label 是在创建figure、table时的label标签 。

`cite{文献名}` ，引用参考文献。

