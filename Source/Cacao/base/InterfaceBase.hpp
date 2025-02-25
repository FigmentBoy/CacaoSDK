// 
// Copyright camila314 & alk1m123 2022. 
//
#pragma once

#include <Base.hpp>
#include <MacroBase.hpp>
#include <PlatformBase.hpp>

#include <Header.hpp>
#include <Cacao.hpp>
#include <Core.hpp>

#include <FunctionBase.hpp>
#include <unordered_map>

#include <type_traits>


#define modContainer (ModInterface::container(STR(PROJECT_NAME)))

template<typename T>
struct field_t {
	template<typename Q>
	void operator=(Q) {
		static_assert(!std::is_same_v<T, T>, "field_t shouldn't be used directly. it should be used with this->*myMember.");
	}

	void operator->() {
		static_assert(!std::is_same_v<T, T>, "field_t shouldn't be used directly. it should be used with this->*myMember.");
	}

	void operator*() {
		static_assert(!std::is_same_v<T, T>, "field_t shouldn't be used directly. it should be used with this->*myMember.");
	} 
};

template<typename T = void*>
struct container_t {
	virtual ~container_t() {
		field.~T();
	}
 	T field;
};

template<typename T, template<typename> typename A1, typename A2>
T& operator->*(A1<A2>* self, field_t<T>& member) {
	// this replaces the destructor in the vtable
	// only done this way to be performant
	auto& dtor = 2[*(size_t**)self]; // i love this
	if (A1<A2>::originalDestructor == 0) {
		A1<A2>::originalDestructor = dtor;
		dtor = (size_t)&A1<A2>::fieldCleanup;
	}

	// gets the respective field
	container_t<>*& field = A1<A2>::fields[(size_t)&member];
	// create the container on first use
	if (!field) field = reinterpret_cast<container_t<>*>(new container_t<T>());
	return reinterpret_cast<container_t<T>*>(field)->field;
}


class InterfaceBase {
public:
	void _apply() {}
	static void fieldCleanup(size_t self) {}
};


template <typename T, typename F>
inline T base_cast(F obj) {
	return static_cast<T>(dynamic_cast<void*>(obj));
}


/**
 * Basic way to make a main function without it being a main
 * function, inject is purposed for that
 */
#define inject() $inject(); static int const _inject = ($inject(), 0); void $inject()


/**
 * Main class implementation, it has the structure
 * 
 * class hook0__;
 * template<typename T>
 * struct _hook0 {};
 * namespace {
 *     struct hook0Unique {};
 *     bool hook0Apply = Cacao::interfaces::$MenuLayer<_hook0<hook0Unique>>::_apply();
 * }
 * using hook0 = _hook0<hook0Unique>;
 * template<>
 * struct hidden _hook0<hook0Unique>: public Cacao::interfaces::$MenuLayer<_hook0<hook0Unique>> {
 *     // code stuff idk
 * };
 * 
 * I tried to make the macro as verbose as it can be but
 * I am bad at this stuff
 */


#define PREDECLARE(derived) derived##__; template<typename T> struct _##derived {};
#define APPLY(base, derived) namespace { struct derived##Unique {}; bool derived##Apply = base<_##derived<derived##Unique> >::_apply();  }
#define DECLARE(base, derived) using derived = _##derived<derived##Unique>; template<> struct hidden _##derived<derived##Unique>: public base<_##derived<derived##Unique> >

#define REDIRECT___(base, derived) PREDECLARE(derived) APPLY(base, derived) DECLARE(base, derived)
#define REDIRECT__(base, derived) REDIRECT___(Cacao::interfaces::$##base, derived)
#define REDIRECT_(base) REDIRECT__(base, CONCAT(hook, __COUNTER__))
#define REDIRECT(base) REDIRECT_(base)

/**
 * Interfaces for the class implementation
 * 
 * $redirect is for when you don't need the name of the class
 * class $redirect(MenuLayer) {};
 * 
 * $implement is for when you need the name of the class
 * class $implement(MenuLayer, MyMenuLayerInterface) {};
 */
#define $redirect(base) REDIRECT(base)
#define $implement(base, derived) REDIRECT__(base, derived)

/**
 * Or just use this lol
 */
#define CRTP1(base) $redirect(base)
#define CRTP2(base, derived) $implement(base, derived)
#define $(...) CONCAT(CRTP, NUMBER_OF_ARGS(__VA_ARGS__))(__VA_ARGS__)

namespace Cacao {
	using namespace cocos2d;
	using namespace cocos2d::extension;
	using std::declval;
	struct interfaces { // i find this really funny
	    #include <Interface.hpp>
	};
}
