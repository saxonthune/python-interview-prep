export type Kind = 'function' | 'class' | 'multi';

export interface BaseProblem {
  id: string;
  topic: string;
  title: string;
  description: string;
  constraints: string;
  skeleton: string;
  kind: Kind;
}

export interface FunctionProblem extends BaseProblem {
  kind: 'function';
  signature: string;
  mutates_input: boolean;
  cases: unknown;
}

export interface ClassProblem extends BaseProblem {
  kind: 'class';
  class_name: string;
  signature: string;
  cases: unknown;
}

export interface MultiProblem extends BaseProblem {
  kind: 'multi';
  function_names: string[];
  cases: Record<string, unknown>;
}

export type Problem = FunctionProblem | ClassProblem | MultiProblem;

import problemsJson from '../../public/problems.json';

export const problems: Problem[] = problemsJson as Problem[];

export function getProblem(id: string): Problem | undefined {
  return problems.find((p) => p.id === id);
}

// Astro getStaticPaths needs filesystem-safe slugs. We replace "/" in the
// problem id with "__" so each problem maps to one route.
export function idToSlug(id: string): string {
  return id.replace(/\//g, '__');
}

export function slugToId(slug: string): string {
  return slug.replace(/__/g, '/');
}
