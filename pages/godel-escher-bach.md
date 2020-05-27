---
layout: page
title: Gödel, Escher, Bach in 34 propositions
permalink: /godel-escher-bach/
published: true
last_updated: 2020-01-02
---

_I originally published this in 2016, after I finished reading the book. I'm republishing it now, with a few edits for clarity, after prompting from [@nosilverv](https://twitter.com/nosilverv), who [asked](https://twitter.com/nosilverv/status/1212716598236254212):_

>  _in GEB did Hofstadter pull various strands together to make a point or did he have a core insight that he then expressed in as many ways as possible?_

_The answer is both, but here I focus on the former. Thanks also to @nosilverv for suggesting the title of this post._

----

Douglas Hofstadter's 1979 masterpiece [*Gödel, Escher, Bach*](goodreads.com/book/show/24113.G_del_Escher_Bach) is notoriously hard to summarize. Its content is no less important than its form—in fact, its content is inextricable from its form. But here we will try to extricate it. Hofstadter would hate seeing these ideas strung out in an ugly skeleton, but even he would admit that most readers misinterpreted his book. In fact, he wrote a whole [_'nuther_ book](https://www.goodreads.com/book/show/123471.I_Am_a_Strange_Loop) to clear up the confusion. (I have not read it, so it's fully possible that I'm just as confused as the rest of them.)

I've attempted to write the core argument in [standardized form](https://www.futurelearn.com/courses/logical-and-critical-thinking/0/steps/9139). "P" stands for "premise", and "C" stands for "conclusion". Some of these claims are vague enough to be nearly meaningless, but that's what you get when you try to compress 777 pages into 34 propositions and you're not a genius. Here goes nothing:

**P1.** The self is the part of the mind that is conscious.

**P2.** The mind is a product of the brain.

**P3.** The brain is composed of neurons.

**P4.** All neuronal activity is either transmission or inhibition of electrical impulses.

**P5.** Electrical impulses carry information.

**P6.** Information is that which can be translated from one form to another, such that the original form could be deduced from the translated form, given a decoding mechanism.

**P7.** The purest way to study the translation and decoding of information is by studying a *formal system*.

**P8.** A formal system is comprised of *axioms*, which are strings of typographical symbols (such as letters), and *rules* for manipulating the axioms to produce *theorems*, which are new strings of symbols.

**P9.** A formal system can be devised such that its typographical symbols correspond to logical or arithmetical words in human language, such as "and", "or", "not", "plus", "equals", etc, and such that the axioms and rules produce theorems which, when interpreted on the level of human language, express only true statements of number theory—e.g. "2+2=4", "13 is prime", "1 /= 0", etc. Hofstadter calls this system Typographical Number Theory (TNT).

**P10.** The symbols of TNT can be arranged so as to *express* (when interpreted on the level of human language) false statements of number theory (such as 1+1=4), but we should not be able to 'decode' (i.e. 'prove') these statements by running the typographical rules backwards to reach the axioms of TNT, because TNT has been deliberately designed to exclude false number-theoretical statements from the range of possible theorems. In other words, TNT has been designed to be consistent (no provable statement is false) and complete (all true statements are provable).

**P11.** Rules for manipulating strings of typographical symbols can do nothing but add, subtract, multiply, or replace typographical symbols.

**P12.** The addition, subtraction, multiplication, or replacement of typographical symbols is precisely what arithmetical operations do.

**C13.** Any formal system can be translated such that its symbols are expressed as numbers and its rules are expressed as arithmetical operations. (This technique is called Gödel-numbering, after the mathematician Kurt Gödel, who invented it. Every string of TNT has a Gödel number.) (by P11 and P12)

**P14.** Two numbers can have a relationship where one is typographically identical to the end of the other—for example, '4' is typographically identical to the end of '1234'.

**P15.** Mathematical proofs can be expressed in TNT.

**P16.** Mathematical proofs that can be expressed in TNT have Gödel numbers.

**P17.** Mathematical proofs end with the statements they prove.

**C18.** The Gödel number of a mathematical proof in TNT would end with the Gödel number of the statement it proves. For example, the proof "premise 1, premise 2, premise 3; therefore, conclusion" might have the Gödel number '1234', and "conclusion" would have the Gödel number '4'. (by P14, P15, P16, and P17)

**P19.** When two Gödel numbers exist such that one is a proof of the other, and the other is identical to the end of the proof (like '1234' and '4'), these numbers can be called a Proof Pair.

**P20.** Statements of number theory can have free variables. For example, "*a* = 1" has the free variable *a*.

**P21.** Since it is possible to express "*a* = 1" as a Gödel number, it is possible to insert that Gödel number into "*a* = 1" as the free variable *a*. (A statement with a free variable is a bit like a predicate with no subject, like "is a sentence fragment." What we're proposing here is like saying "'is a sentence fragment' is a sentence fragment." Hofstadter calls this self-referential sentence the _Arithmoquinification_ of *a*. The word comes from two ideas:

1. For a sentence to "quine" is for a sentence to quote itself, as in "'is a sentence fragment' is a sentence fragment" (after the logician Willard Van Orman Quine)
2. The "Arithmo" in "Arithmoquine" signifies that a string of symbols is quining, but arithmetically, as in the Gödel number for "'*a* = 1' = 1".

**P22.** You can make the statement, "There are two numbers such that one is the Arithmoquinification of the other." (Like saying, "there are two strings of words such that one is the quinification of the other" or "there is a sentence which quotes itself"). This statement, like all number-theoretical statements, has a Gödel number.

**P23.** You can make the statement that "There are no two numbers such that a) they form a Proof Pair (i.e. one is the Gödel number of the conclusion of a proof whose Gödel number ends in that first number, as in '4' and '1234', hypothetically), and b) one is the Arithmoquinification of the other (i.e. one is the same as the other except that it has inserted itself into its free variable, as in "'is a sentence fragment' is a sentence fragment").

**P24.** The string of TNT-symbols that expresses the above statement (in P23) has a Gödel number, and it has a free variable (namely the first number in the statement in P22), which means it can be Arithmoquined (i.e. its free variable can be replaced by itself). (Uh oh.)

**P25.** If you *do* Arithmoquine the statement in P23, then you get the following: "There is no Proof Pair ending in the Arithmoquinification of the statement in P23."

**P26.** The statement in P25 means, "There is no proof of this statement."

**P27.** In other words, "I am not provable in TNT." (Note that we have not *derived* this statement from the axioms of TNT. We've only *expressed* it, with the faith that all theorems of TNT are true statements of number theory and that all true statements of number theory are theorems of TNT.)

**P28.** But if "I am not provable in TNT" is *true*, then all true statements of number theory are not represented (i.e. provable) in the theorems of TNT.

**P29.** And if "I am not provable in TNT" is *false*, then that precise statement must be provable in TNT, which means that not all theorems of TNT are true.

**C30.** (And this is Gödel's first incompleteness theorem:) Any formal system that is sufficiently sophisticated to express truths of number theory cannot be both consistent and complete. (That is, as soon as it gains the power to refer to itself, TNT explodes! #pun) (by P19-P29)

**P31.** (And here's where the airtightness of Hofstadter's argument also explodes, but beautifully:) There is a deep, abstract likeness between a) the information that is carried and manipulated by neurons and b) the information that is carried and manipulated by the rules of a formal system.

**P32.** Selfless ingredients, when subjected to sufficiently sophisticated rules of manipulation, acquire the ability to indirectly refer to themselves and the system which produces them.

**P33.** The electrical signals in human brains (selfless ingredients) are subject to (surely highly sophisticated) rules of manipulation via neurons.

**C34.** Perhaps our sense of self—our subjective experience of the world, our feeling that there is an "I" who is perceiving everything—emerges in our brains as inexorably as self-reference emerges out of formal systems such as TNT, and in an analogous way. (by C30, P31, P32, and P33)

It's not exactly a _convincing_ argument... but at least it makes you feel smart. Really though, GEB is more about beauty than it is about linear cogency. 6 out of 5 stars. Read it!