/****************************************************************************
 * IVisitor.h
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 *
 ****************************************************************************/
#pragma once

namespace zsp {
namespace ast {

class ITemplateParamValueList;
class ITemplateParamValue;
class IRefExpr;
class IExprAggrMapElem;
class IExprAggrStructElem;
class IActivityJoinSpec;
class ISymbolImportSpec;
class IExecTargetTemplateParam;
class IAssocData;
class ISymbolRefPath;
class IScopeChild;
class IActivitySelectBranch;
class IActivityMatchChoice;
class ITemplateParamDeclList;
class IExpr;
class IExprStaticRefPath;
class IActivityStmt;
class IActivitySchedulingConstraint;
class IExprString;
class IExprSubscript;
class IExprUnary;
class IMethodParameterList;
class ITypeIdentifier;
class ITypeIdentifierElem;
class IFunctionDefinition;
class IFunctionParamDecl;
class IActivityJoinSpecBranch;
class IActivityJoinSpecSelect;
class IActivityJoinSpecNone;
class IActivityJoinSpecFirst;
class IFunctionImport;
class IScope;
class IScopeChildRef;
class INamedScopeChild;
class IPackageImportStmt;
class IPyImportStmt;
class IPyImportFromStmt;
class ITemplateParamDecl;
class IConstraintStmt;
class ITemplateParamTypeValue;
class ITemplateParamExprValue;
class IExtendEnum;
class IExecStmt;
class IExecTargetTemplateBlock;
class IProceduralStmtIfClause;
class IRefExprTypeScopeGlobal;
class IRefExprTypeScopeContext;
class IRefExprScopeIndex;
class ISymbolChild;
class ISymbolScopeRef;
class IDataType;
class IExprAggrLiteral;
class IExprBin;
class IExprBitSlice;
class IExprBool;
class IExprCast;
class IExprCompileHas;
class IExprCond;
class IExprDomainOpenRangeList;
class IExprDomainOpenRangeValue;
class IExprHierarchicalId;
class IExprId;
class IExprIn;
class IExprListLiteral;
class IExprStructLiteral;
class IExprStructLiteralItem;
class IExprMemberPathElem;
class IExprNull;
class IExprNumber;
class IExprOpenRangeList;
class IExprOpenRangeValue;
class IExprRefPath;
class IExprRefPathElem;
class IExprSignedNumber;
class IActivityBindStmt;
class IActivityConstraint;
class IActivityLabeledStmt;
class IExprUnsignedNumber;
class IFunctionPrototype;
class IFunctionImportType;
class IFunctionImportProto;
class IGlobalScope;
class INamedScope;
class IPackageScope;
class IConstraintScope;
class ITemplateGenericTypeParamDecl;
class ITemplateCategoryTypeParamDecl;
class ITemplateValueParamDecl;
class IConstraintStmtExpr;
class IConstraintStmtField;
class IConstraintStmtIf;
class IExtendType;
class IConstraintStmtUnique;
class IField;
class IFieldCompRef;
class IFieldRef;
class IFieldClaim;
class IConstraintStmtDefault;
class IConstraintStmtDefaultDisable;
class IProceduralStmtAssignment;
class IProceduralStmtExpr;
class IProceduralStmtFunctionCall;
class IProceduralStmtReturn;
class IProceduralStmtBody;
class IProceduralStmtIfElse;
class IProceduralStmtMatch;
class IProceduralStmtMatchChoice;
class IProceduralStmtBreak;
class IProceduralStmtContinue;
class IProceduralStmtDataDeclaration;
class IProceduralStmtYield;
class ISymbolChildrenScope;
class IDataTypeBool;
class IDataTypeChandle;
class IDataTypeEnum;
class IEnumItem;
class IEnumDecl;
class IDataTypeInt;
class IDataTypePyObj;
class IDataTypeRef;
class IDataTypeString;
class IDataTypeUserDefined;
class IExprAggrEmpty;
class IExprAggrList;
class IExprAggrMap;
class IExprAggrStruct;
class IExprRefPathId;
class IExprRefPathContext;
class IExprRefPathStatic;
class IExprRefPathStaticRooted;
class ITypeScope;
class IActivityActionHandleTraversal;
class IActivityActionTypeTraversal;
class IActivityRepeatCount;
class IActivityRepeatWhile;
class IActivityForeach;
class IActivitySelect;
class IActivityIfElse;
class IActivityMatch;
class IActivityReplicate;
class IActivitySuper;
class IConstraintBlock;
class IConstraintStmtForeach;
class IConstraintStmtForall;
class IConstraintStmtImplication;
class IProceduralStmtRepeatWhile;
class IProceduralStmtWhile;
class ISymbolScope;
class IExprRefPathStaticFunc;
class IExprRefPathSuper;
class IProceduralStmtSymbolBodyScope;
class IActivityDecl;
class IStruct;
class IActivityLabeledScope;
class IRootSymbolScope;
class IExecScope;
class ISymbolEnumScope;
class ISymbolExtendScope;
class ISymbolTypeScope;
class ISymbolFunctionScope;
class IAction;
class IComponent;
class IConstraintSymbolScope;
class IActivitySequence;
class IExecBlock;
class IActivityParallel;
class IActivitySchedule;
class IProceduralStmtRepeat;
class IProceduralStmtForeach;

class TemplateParamValueList;
class TemplateParamValue;
class RefExpr;
class ExprAggrMapElem;
class ExprAggrStructElem;
class ActivityJoinSpec;
class SymbolImportSpec;
class ExecTargetTemplateParam;
class AssocData;
class SymbolRefPath;
class ScopeChild;
class ActivitySelectBranch;
class ActivityMatchChoice;
class TemplateParamDeclList;
class Expr;
class ExprStaticRefPath;
class ActivityStmt;
class ActivitySchedulingConstraint;
class ExprString;
class ExprSubscript;
class ExprUnary;
class MethodParameterList;
class TypeIdentifier;
class TypeIdentifierElem;
class FunctionDefinition;
class FunctionParamDecl;
class ActivityJoinSpecBranch;
class ActivityJoinSpecSelect;
class ActivityJoinSpecNone;
class ActivityJoinSpecFirst;
class FunctionImport;
class Scope;
class ScopeChildRef;
class NamedScopeChild;
class PackageImportStmt;
class PyImportStmt;
class PyImportFromStmt;
class TemplateParamDecl;
class ConstraintStmt;
class TemplateParamTypeValue;
class TemplateParamExprValue;
class ExtendEnum;
class ExecStmt;
class ExecTargetTemplateBlock;
class ProceduralStmtIfClause;
class RefExprTypeScopeGlobal;
class RefExprTypeScopeContext;
class RefExprScopeIndex;
class SymbolChild;
class SymbolScopeRef;
class DataType;
class ExprAggrLiteral;
class ExprBin;
class ExprBitSlice;
class ExprBool;
class ExprCast;
class ExprCompileHas;
class ExprCond;
class ExprDomainOpenRangeList;
class ExprDomainOpenRangeValue;
class ExprHierarchicalId;
class ExprId;
class ExprIn;
class ExprListLiteral;
class ExprStructLiteral;
class ExprStructLiteralItem;
class ExprMemberPathElem;
class ExprNull;
class ExprNumber;
class ExprOpenRangeList;
class ExprOpenRangeValue;
class ExprRefPath;
class ExprRefPathElem;
class ExprSignedNumber;
class ActivityBindStmt;
class ActivityConstraint;
class ActivityLabeledStmt;
class ExprUnsignedNumber;
class FunctionPrototype;
class FunctionImportType;
class FunctionImportProto;
class GlobalScope;
class NamedScope;
class PackageScope;
class ConstraintScope;
class TemplateGenericTypeParamDecl;
class TemplateCategoryTypeParamDecl;
class TemplateValueParamDecl;
class ConstraintStmtExpr;
class ConstraintStmtField;
class ConstraintStmtIf;
class ExtendType;
class ConstraintStmtUnique;
class Field;
class FieldCompRef;
class FieldRef;
class FieldClaim;
class ConstraintStmtDefault;
class ConstraintStmtDefaultDisable;
class ProceduralStmtAssignment;
class ProceduralStmtExpr;
class ProceduralStmtFunctionCall;
class ProceduralStmtReturn;
class ProceduralStmtBody;
class ProceduralStmtIfElse;
class ProceduralStmtMatch;
class ProceduralStmtMatchChoice;
class ProceduralStmtBreak;
class ProceduralStmtContinue;
class ProceduralStmtDataDeclaration;
class ProceduralStmtYield;
class SymbolChildrenScope;
class DataTypeBool;
class DataTypeChandle;
class DataTypeEnum;
class EnumItem;
class EnumDecl;
class DataTypeInt;
class DataTypePyObj;
class DataTypeRef;
class DataTypeString;
class DataTypeUserDefined;
class ExprAggrEmpty;
class ExprAggrList;
class ExprAggrMap;
class ExprAggrStruct;
class ExprRefPathId;
class ExprRefPathContext;
class ExprRefPathStatic;
class ExprRefPathStaticRooted;
class TypeScope;
class ActivityActionHandleTraversal;
class ActivityActionTypeTraversal;
class ActivityRepeatCount;
class ActivityRepeatWhile;
class ActivityForeach;
class ActivitySelect;
class ActivityIfElse;
class ActivityMatch;
class ActivityReplicate;
class ActivitySuper;
class ConstraintBlock;
class ConstraintStmtForeach;
class ConstraintStmtForall;
class ConstraintStmtImplication;
class ProceduralStmtRepeatWhile;
class ProceduralStmtWhile;
class SymbolScope;
class ExprRefPathStaticFunc;
class ExprRefPathSuper;
class ProceduralStmtSymbolBodyScope;
class ActivityDecl;
class Struct;
class ActivityLabeledScope;
class RootSymbolScope;
class ExecScope;
class SymbolEnumScope;
class SymbolExtendScope;
class SymbolTypeScope;
class SymbolFunctionScope;
class Action;
class Component;
class ConstraintSymbolScope;
class ActivitySequence;
class ExecBlock;
class ActivityParallel;
class ActivitySchedule;
class ProceduralStmtRepeat;
class ProceduralStmtForeach;

class IVisitor {
public:
    virtual ~IVisitor() { }
    
    virtual void visitTemplateParamValueList(ITemplateParamValueList *i) = 0;
    
    virtual void visitTemplateParamValue(ITemplateParamValue *i) = 0;
    
    virtual void visitRefExpr(IRefExpr *i) = 0;
    
    virtual void visitExprAggrMapElem(IExprAggrMapElem *i) = 0;
    
    virtual void visitExprAggrStructElem(IExprAggrStructElem *i) = 0;
    
    virtual void visitActivityJoinSpec(IActivityJoinSpec *i) = 0;
    
    virtual void visitSymbolImportSpec(ISymbolImportSpec *i) = 0;
    
    virtual void visitExecTargetTemplateParam(IExecTargetTemplateParam *i) = 0;
    
    virtual void visitAssocData(IAssocData *i) = 0;
    
    virtual void visitSymbolRefPath(ISymbolRefPath *i) = 0;
    
    virtual void visitScopeChild(IScopeChild *i) = 0;
    
    virtual void visitActivitySelectBranch(IActivitySelectBranch *i) = 0;
    
    virtual void visitActivityMatchChoice(IActivityMatchChoice *i) = 0;
    
    virtual void visitTemplateParamDeclList(ITemplateParamDeclList *i) = 0;
    
    virtual void visitExpr(IExpr *i) = 0;
    
    virtual void visitExprStaticRefPath(IExprStaticRefPath *i) = 0;
    
    virtual void visitActivityStmt(IActivityStmt *i) = 0;
    
    virtual void visitActivitySchedulingConstraint(IActivitySchedulingConstraint *i) = 0;
    
    virtual void visitExprString(IExprString *i) = 0;
    
    virtual void visitExprSubscript(IExprSubscript *i) = 0;
    
    virtual void visitExprUnary(IExprUnary *i) = 0;
    
    virtual void visitMethodParameterList(IMethodParameterList *i) = 0;
    
    virtual void visitTypeIdentifier(ITypeIdentifier *i) = 0;
    
    virtual void visitTypeIdentifierElem(ITypeIdentifierElem *i) = 0;
    
    virtual void visitFunctionDefinition(IFunctionDefinition *i) = 0;
    
    virtual void visitFunctionParamDecl(IFunctionParamDecl *i) = 0;
    
    virtual void visitActivityJoinSpecBranch(IActivityJoinSpecBranch *i) = 0;
    
    virtual void visitActivityJoinSpecSelect(IActivityJoinSpecSelect *i) = 0;
    
    virtual void visitActivityJoinSpecNone(IActivityJoinSpecNone *i) = 0;
    
    virtual void visitActivityJoinSpecFirst(IActivityJoinSpecFirst *i) = 0;
    
    virtual void visitFunctionImport(IFunctionImport *i) = 0;
    
    virtual void visitScope(IScope *i) = 0;
    
    virtual void visitScopeChildRef(IScopeChildRef *i) = 0;
    
    virtual void visitNamedScopeChild(INamedScopeChild *i) = 0;
    
    virtual void visitPackageImportStmt(IPackageImportStmt *i) = 0;
    
    virtual void visitPyImportStmt(IPyImportStmt *i) = 0;
    
    virtual void visitPyImportFromStmt(IPyImportFromStmt *i) = 0;
    
    virtual void visitTemplateParamDecl(ITemplateParamDecl *i) = 0;
    
    virtual void visitConstraintStmt(IConstraintStmt *i) = 0;
    
    virtual void visitTemplateParamTypeValue(ITemplateParamTypeValue *i) = 0;
    
    virtual void visitTemplateParamExprValue(ITemplateParamExprValue *i) = 0;
    
    virtual void visitExtendEnum(IExtendEnum *i) = 0;
    
    virtual void visitExecStmt(IExecStmt *i) = 0;
    
    virtual void visitExecTargetTemplateBlock(IExecTargetTemplateBlock *i) = 0;
    
    virtual void visitProceduralStmtIfClause(IProceduralStmtIfClause *i) = 0;
    
    virtual void visitRefExprTypeScopeGlobal(IRefExprTypeScopeGlobal *i) = 0;
    
    virtual void visitRefExprTypeScopeContext(IRefExprTypeScopeContext *i) = 0;
    
    virtual void visitRefExprScopeIndex(IRefExprScopeIndex *i) = 0;
    
    virtual void visitSymbolChild(ISymbolChild *i) = 0;
    
    virtual void visitSymbolScopeRef(ISymbolScopeRef *i) = 0;
    
    virtual void visitDataType(IDataType *i) = 0;
    
    virtual void visitExprAggrLiteral(IExprAggrLiteral *i) = 0;
    
    virtual void visitExprBin(IExprBin *i) = 0;
    
    virtual void visitExprBitSlice(IExprBitSlice *i) = 0;
    
    virtual void visitExprBool(IExprBool *i) = 0;
    
    virtual void visitExprCast(IExprCast *i) = 0;
    
    virtual void visitExprCompileHas(IExprCompileHas *i) = 0;
    
    virtual void visitExprCond(IExprCond *i) = 0;
    
    virtual void visitExprDomainOpenRangeList(IExprDomainOpenRangeList *i) = 0;
    
    virtual void visitExprDomainOpenRangeValue(IExprDomainOpenRangeValue *i) = 0;
    
    virtual void visitExprHierarchicalId(IExprHierarchicalId *i) = 0;
    
    virtual void visitExprId(IExprId *i) = 0;
    
    virtual void visitExprIn(IExprIn *i) = 0;
    
    virtual void visitExprListLiteral(IExprListLiteral *i) = 0;
    
    virtual void visitExprStructLiteral(IExprStructLiteral *i) = 0;
    
    virtual void visitExprStructLiteralItem(IExprStructLiteralItem *i) = 0;
    
    virtual void visitExprMemberPathElem(IExprMemberPathElem *i) = 0;
    
    virtual void visitExprNull(IExprNull *i) = 0;
    
    virtual void visitExprNumber(IExprNumber *i) = 0;
    
    virtual void visitExprOpenRangeList(IExprOpenRangeList *i) = 0;
    
    virtual void visitExprOpenRangeValue(IExprOpenRangeValue *i) = 0;
    
    virtual void visitExprRefPath(IExprRefPath *i) = 0;
    
    virtual void visitExprRefPathElem(IExprRefPathElem *i) = 0;
    
    virtual void visitExprSignedNumber(IExprSignedNumber *i) = 0;
    
    virtual void visitActivityBindStmt(IActivityBindStmt *i) = 0;
    
    virtual void visitActivityConstraint(IActivityConstraint *i) = 0;
    
    virtual void visitActivityLabeledStmt(IActivityLabeledStmt *i) = 0;
    
    virtual void visitExprUnsignedNumber(IExprUnsignedNumber *i) = 0;
    
    virtual void visitFunctionPrototype(IFunctionPrototype *i) = 0;
    
    virtual void visitFunctionImportType(IFunctionImportType *i) = 0;
    
    virtual void visitFunctionImportProto(IFunctionImportProto *i) = 0;
    
    virtual void visitGlobalScope(IGlobalScope *i) = 0;
    
    virtual void visitNamedScope(INamedScope *i) = 0;
    
    virtual void visitPackageScope(IPackageScope *i) = 0;
    
    virtual void visitConstraintScope(IConstraintScope *i) = 0;
    
    virtual void visitTemplateGenericTypeParamDecl(ITemplateGenericTypeParamDecl *i) = 0;
    
    virtual void visitTemplateCategoryTypeParamDecl(ITemplateCategoryTypeParamDecl *i) = 0;
    
    virtual void visitTemplateValueParamDecl(ITemplateValueParamDecl *i) = 0;
    
    virtual void visitConstraintStmtExpr(IConstraintStmtExpr *i) = 0;
    
    virtual void visitConstraintStmtField(IConstraintStmtField *i) = 0;
    
    virtual void visitConstraintStmtIf(IConstraintStmtIf *i) = 0;
    
    virtual void visitExtendType(IExtendType *i) = 0;
    
    virtual void visitConstraintStmtUnique(IConstraintStmtUnique *i) = 0;
    
    virtual void visitField(IField *i) = 0;
    
    virtual void visitFieldCompRef(IFieldCompRef *i) = 0;
    
    virtual void visitFieldRef(IFieldRef *i) = 0;
    
    virtual void visitFieldClaim(IFieldClaim *i) = 0;
    
    virtual void visitConstraintStmtDefault(IConstraintStmtDefault *i) = 0;
    
    virtual void visitConstraintStmtDefaultDisable(IConstraintStmtDefaultDisable *i) = 0;
    
    virtual void visitProceduralStmtAssignment(IProceduralStmtAssignment *i) = 0;
    
    virtual void visitProceduralStmtExpr(IProceduralStmtExpr *i) = 0;
    
    virtual void visitProceduralStmtFunctionCall(IProceduralStmtFunctionCall *i) = 0;
    
    virtual void visitProceduralStmtReturn(IProceduralStmtReturn *i) = 0;
    
    virtual void visitProceduralStmtBody(IProceduralStmtBody *i) = 0;
    
    virtual void visitProceduralStmtIfElse(IProceduralStmtIfElse *i) = 0;
    
    virtual void visitProceduralStmtMatch(IProceduralStmtMatch *i) = 0;
    
    virtual void visitProceduralStmtMatchChoice(IProceduralStmtMatchChoice *i) = 0;
    
    virtual void visitProceduralStmtBreak(IProceduralStmtBreak *i) = 0;
    
    virtual void visitProceduralStmtContinue(IProceduralStmtContinue *i) = 0;
    
    virtual void visitProceduralStmtDataDeclaration(IProceduralStmtDataDeclaration *i) = 0;
    
    virtual void visitProceduralStmtYield(IProceduralStmtYield *i) = 0;
    
    virtual void visitSymbolChildrenScope(ISymbolChildrenScope *i) = 0;
    
    virtual void visitDataTypeBool(IDataTypeBool *i) = 0;
    
    virtual void visitDataTypeChandle(IDataTypeChandle *i) = 0;
    
    virtual void visitDataTypeEnum(IDataTypeEnum *i) = 0;
    
    virtual void visitEnumItem(IEnumItem *i) = 0;
    
    virtual void visitEnumDecl(IEnumDecl *i) = 0;
    
    virtual void visitDataTypeInt(IDataTypeInt *i) = 0;
    
    virtual void visitDataTypePyObj(IDataTypePyObj *i) = 0;
    
    virtual void visitDataTypeRef(IDataTypeRef *i) = 0;
    
    virtual void visitDataTypeString(IDataTypeString *i) = 0;
    
    virtual void visitDataTypeUserDefined(IDataTypeUserDefined *i) = 0;
    
    virtual void visitExprAggrEmpty(IExprAggrEmpty *i) = 0;
    
    virtual void visitExprAggrList(IExprAggrList *i) = 0;
    
    virtual void visitExprAggrMap(IExprAggrMap *i) = 0;
    
    virtual void visitExprAggrStruct(IExprAggrStruct *i) = 0;
    
    virtual void visitExprRefPathId(IExprRefPathId *i) = 0;
    
    virtual void visitExprRefPathContext(IExprRefPathContext *i) = 0;
    
    virtual void visitExprRefPathStatic(IExprRefPathStatic *i) = 0;
    
    virtual void visitExprRefPathStaticRooted(IExprRefPathStaticRooted *i) = 0;
    
    virtual void visitTypeScope(ITypeScope *i) = 0;
    
    virtual void visitActivityActionHandleTraversal(IActivityActionHandleTraversal *i) = 0;
    
    virtual void visitActivityActionTypeTraversal(IActivityActionTypeTraversal *i) = 0;
    
    virtual void visitActivityRepeatCount(IActivityRepeatCount *i) = 0;
    
    virtual void visitActivityRepeatWhile(IActivityRepeatWhile *i) = 0;
    
    virtual void visitActivityForeach(IActivityForeach *i) = 0;
    
    virtual void visitActivitySelect(IActivitySelect *i) = 0;
    
    virtual void visitActivityIfElse(IActivityIfElse *i) = 0;
    
    virtual void visitActivityMatch(IActivityMatch *i) = 0;
    
    virtual void visitActivityReplicate(IActivityReplicate *i) = 0;
    
    virtual void visitActivitySuper(IActivitySuper *i) = 0;
    
    virtual void visitConstraintBlock(IConstraintBlock *i) = 0;
    
    virtual void visitConstraintStmtForeach(IConstraintStmtForeach *i) = 0;
    
    virtual void visitConstraintStmtForall(IConstraintStmtForall *i) = 0;
    
    virtual void visitConstraintStmtImplication(IConstraintStmtImplication *i) = 0;
    
    virtual void visitProceduralStmtRepeatWhile(IProceduralStmtRepeatWhile *i) = 0;
    
    virtual void visitProceduralStmtWhile(IProceduralStmtWhile *i) = 0;
    
    virtual void visitSymbolScope(ISymbolScope *i) = 0;
    
    virtual void visitExprRefPathStaticFunc(IExprRefPathStaticFunc *i) = 0;
    
    virtual void visitExprRefPathSuper(IExprRefPathSuper *i) = 0;
    
    virtual void visitProceduralStmtSymbolBodyScope(IProceduralStmtSymbolBodyScope *i) = 0;
    
    virtual void visitActivityDecl(IActivityDecl *i) = 0;
    
    virtual void visitStruct(IStruct *i) = 0;
    
    virtual void visitActivityLabeledScope(IActivityLabeledScope *i) = 0;
    
    virtual void visitRootSymbolScope(IRootSymbolScope *i) = 0;
    
    virtual void visitExecScope(IExecScope *i) = 0;
    
    virtual void visitSymbolEnumScope(ISymbolEnumScope *i) = 0;
    
    virtual void visitSymbolExtendScope(ISymbolExtendScope *i) = 0;
    
    virtual void visitSymbolTypeScope(ISymbolTypeScope *i) = 0;
    
    virtual void visitSymbolFunctionScope(ISymbolFunctionScope *i) = 0;
    
    virtual void visitAction(IAction *i) = 0;
    
    virtual void visitComponent(IComponent *i) = 0;
    
    virtual void visitConstraintSymbolScope(IConstraintSymbolScope *i) = 0;
    
    virtual void visitActivitySequence(IActivitySequence *i) = 0;
    
    virtual void visitExecBlock(IExecBlock *i) = 0;
    
    virtual void visitActivityParallel(IActivityParallel *i) = 0;
    
    virtual void visitActivitySchedule(IActivitySchedule *i) = 0;
    
    virtual void visitProceduralStmtRepeat(IProceduralStmtRepeat *i) = 0;
    
    virtual void visitProceduralStmtForeach(IProceduralStmtForeach *i) = 0;
    
};

} // namespace zsp
} // namespace ast

